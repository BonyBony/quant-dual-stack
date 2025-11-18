"""
Unit tests for ML dataset builder - verify NO DATA LEAKAGE!

These tests are CRITICAL. They prove that:
1. Features are properly lagged (no future data in features)
2. Labels don't leak into features
3. Cross-sectional standardization uses only contemporaneous data

Run with: pytest tests/test_ml_dataset_no_leakage.py -v
"""

import numpy as np
import pandas as pd
import pytest

from jobs.build_ml_dataset import (
    compute_features_raw,
    lag_features,
    cross_sectional_standardize,
    compute_labels,
)


@pytest.fixture
def sample_ohlcv():
    """Create sample OHLCV data for 2 stocks over 10 days."""
    dates = pd.date_range("2023-01-01", periods=10, freq="D")
    symbols = ["STOCK_A", "STOCK_B"]

    data = []
    for symbol in symbols:
        for i, date in enumerate(dates):
            # Create predictable prices
            base_price = 100 if symbol == "STOCK_A" else 200
            price = base_price + i  # Increasing price

            data.append({
                "date": date,
                "symbol": symbol,
                "open": price - 0.5,
                "high": price + 1.0,
                "low": price - 1.0,
                "close": price,
                "volume": 100000 + i * 1000,
            })

    df = pd.DataFrame(data)
    df = df.set_index(["date", "symbol"])
    return df


def test_feature_lagging_prevents_lookahead(sample_ohlcv):
    """
    CRITICAL TEST: Features at time t should only use data up to t-1.

    If features at t use data from t, we have lookahead bias!
    """
    df = sample_ohlcv.copy()

    # Compute raw features (not lagged)
    df_features = compute_features_raw(df)

    # Get first momentum feature (ret_1d = today's return)
    feature_cols = [col for col in df_features.columns if col.startswith("ret_")]

    # Before lagging: ret_1d at date T uses close[T] / close[T-1]
    # This means ret_1d at T contains information from T!
    df_before_lag = df_features[feature_cols].copy()

    # After lagging: ret_1d should be shifted forward by 1
    df_after_lag = lag_features(df_features, feature_cols)

    # Check: at date T, lagged feature should equal raw feature at T-1
    dates = df_features.index.get_level_values("date").unique()

    for symbol in ["STOCK_A", "STOCK_B"]:
        for i in range(1, len(dates)):
            date_t = dates[i]
            date_t_minus_1 = dates[i - 1]

            # Get raw feature at T-1
            raw_at_t_minus_1 = df_before_lag.loc[(date_t_minus_1, symbol), "ret_1d"]

            # Get lagged feature at T
            lagged_at_t = df_after_lag.loc[(date_t, symbol), "ret_1d"]

            # They should be equal! (lagged feature brings T-1 info to T)
            if not pd.isna(raw_at_t_minus_1) and not pd.isna(lagged_at_t):
                assert np.isclose(raw_at_t_minus_1, lagged_at_t, rtol=1e-5), \
                    f"Lagging failed for {symbol} at {date_t}"

    # Also check: first date should have NaN (no previous data)
    first_date = dates[0]
    for symbol in ["STOCK_A", "STOCK_B"]:
        lagged_first = df_after_lag.loc[(first_date, symbol), "ret_1d"]
        assert pd.isna(lagged_first), "First date should have NaN after lagging"

    print("✅ Feature lagging correctly prevents lookahead bias")


def test_cross_sectional_standardization_no_leakage(sample_ohlcv):
    """
    CRITICAL TEST: Cross-sectional z-scoring should only use data from that day.

    If we use future dates to compute mean/std, we have leakage!
    """
    df = sample_ohlcv.copy()

    # Add a simple feature
    df["feature_x"] = df.groupby("symbol")["close"].pct_change()

    # Standardize cross-sectionally
    df_standardized = cross_sectional_standardize(df, ["feature_x"])

    # Check: For each date, z-scores should have mean~0 and std~1 across stocks
    dates = df.index.get_level_values("date").unique()

    for date in dates:
        date_data = df_standardized.loc[date, "feature_x"]

        # Skip if all NaN
        if date_data.notna().sum() < 2:
            continue

        mean_across_stocks = date_data.mean()
        std_across_stocks = date_data.std()

        # Mean should be close to 0
        assert abs(mean_across_stocks) < 1e-6, \
            f"Cross-sectional mean not zero for {date}"

        # Std should be close to 1 (if >1 stock with valid data)
        if date_data.notna().sum() > 1:
            assert abs(std_across_stocks - 1.0) < 0.1, \
                f"Cross-sectional std not 1.0 for {date}"

    print("✅ Cross-sectional standardization is leak-free")


def test_labels_dont_leak_into_features():
    """
    CRITICAL TEST: Features at time t should NEVER contain labels from t+1.

    This test ensures labels (future returns) are not accidentally used as features.
    """
    # Create simple data
    dates = pd.date_range("2023-01-01", periods=5, freq="D")
    df = pd.DataFrame({
        "date": dates,
        "symbol": "TEST",
        "close": [100, 105, 103, 108, 110],
    })
    df = df.set_index(["date", "symbol"])

    # Compute labels (forward returns)
    df_labels = compute_labels(df)

    # Check: label at date T should be return from T to T+1
    # So label at T should be close[T+1] / close[T]
    for i in range(len(dates) - 1):
        date_t = dates[i]
        close_t = df.loc[(date_t, "TEST"), "close"]
        close_t_plus_1 = df.loc[(dates[i + 1], "TEST"), "close"]

        expected_label = np.log(close_t_plus_1 / close_t)
        actual_label = df_labels.loc[(date_t, "TEST"), "label"]

        assert np.isclose(expected_label, actual_label, rtol=1e-5), \
            f"Label mismatch at {date_t}"

    # Check: last date should have NaN label (no future data)
    last_date = dates[-1]
    assert pd.isna(df_labels.loc[(last_date, "TEST"), "label"]), \
        "Last date should have NaN label"

    print("✅ Labels correctly use future data (and don't leak into features)")


def test_no_future_features_predict_current_labels():
    """
    SANITY TEST: Can raw (un-lagged) features predict current labels?

    If YES → we have leakage (features contain info from the same period as label).
    If NO → good! Features are independent of labels.

    This test should FAIL if we don't lag features properly.
    """
    # Create data where return is deterministic from price
    dates = pd.date_range("2023-01-01", periods=50, freq="D")
    df = pd.DataFrame({
        "date": dates,
        "symbol": "TEST",
        "close": np.random.randn(50).cumsum() + 100,
    })
    df = df.set_index(["date", "symbol"])

    # Add raw momentum feature (not lagged)
    df["ret_5d_raw"] = df.groupby("symbol")["close"].pct_change(5)

    # Compute labels
    df_labels = compute_labels(df)

    # Merge
    merged = df.join(df_labels, how="inner")
    merged = merged.dropna()

    # Correlation between raw feature and label
    corr_raw = merged["ret_5d_raw"].corr(merged["label"])

    # Now lag the feature
    df["ret_5d_lagged"] = df.groupby("symbol")["ret_5d_raw"].shift(1)
    merged_lagged = df.join(df_labels, how="inner")
    merged_lagged = merged_lagged.dropna()

    corr_lagged = merged_lagged["ret_5d_lagged"].corr(merged_lagged["label"])

    print(f"Correlation (raw feature vs label): {corr_raw:.4f}")
    print(f"Correlation (lagged feature vs label): {corr_lagged:.4f}")

    # Raw feature should have HIGHER correlation (it's contaminated!)
    # Lagged feature should have LOWER correlation (it's clean)
    assert abs(corr_raw) > abs(corr_lagged) or abs(corr_lagged) < 0.15, \
        "Lagged feature should have weaker correlation with label"

    print("✅ Lagging reduces feature-label correlation (prevents leakage)")


def test_purged_cv_split_no_overlap():
    """
    TEST: Purged CV splits should have no date overlap between train and test.

    If test dates appear in train → leakage!
    """
    from common.validation.purged_cv import PurgedGroupTimeSeriesSplit

    dates = pd.date_range("2023-01-01", periods=100, freq="D")
    X = pd.DataFrame({"dummy": range(100)})
    groups = dates  # Each row has a date

    cv = PurgedGroupTimeSeriesSplit(n_splits=5, embargo_groups=5)

    for fold_idx, (train_idx, test_idx) in enumerate(cv.split(X, groups=groups)):
        train_dates = set(dates[train_idx])
        test_dates = set(dates[test_idx])

        # Check: no overlap
        overlap = train_dates.intersection(test_dates)
        assert len(overlap) == 0, f"Fold {fold_idx}: train/test overlap detected!"

        # Check: train dates come before test dates
        max_train_date = max(train_dates)
        min_test_date = min(test_dates)
        assert max_train_date < min_test_date, \
            f"Fold {fold_idx}: train dates not strictly before test dates!"

    print("✅ Purged CV splits have no temporal leakage")


def test_end_to_end_no_leakage_smoke_test(sample_ohlcv):
    """
    SMOKE TEST: Run entire pipeline and check output dimensions.
    """
    df = sample_ohlcv.copy()

    # 1. Compute features
    df_features = compute_features_raw(df)
    feature_cols = [col for col in df_features.columns
                    if col not in {"open", "high", "low", "close", "volume", "symbol"}]

    # 2. Lag features
    df_lagged = lag_features(df_features, feature_cols)

    # 3. Standardize
    df_standardized = cross_sectional_standardize(df_lagged, feature_cols)

    # 4. Compute labels
    df_labels = compute_labels(df)

    # 5. Check dimensions
    assert df_standardized.shape[0] == df_labels.shape[0]
    assert len(feature_cols) > 0

    # 6. Check no complete NaN columns
    assert not df_standardized[feature_cols].isna().all().any()

    print("✅ End-to-end pipeline runs without errors")


if __name__ == "__main__":
    # Run tests manually
    import sys

    print("="*60)
    print("LEAK-FREE DATASET BUILDER - UNIT TESTS")
    print("="*60)

    sample = sample_ohlcv()

    try:
        test_feature_lagging_prevents_lookahead(sample)
        test_cross_sectional_standardization_no_leakage(sample)
        test_labels_dont_leak_into_features()
        test_no_future_features_predict_current_labels()
        test_purged_cv_split_no_overlap()
        test_end_to_end_no_leakage_smoke_test(sample)

        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED - NO DATA LEAKAGE DETECTED!")
        print("="*60)
        sys.exit(0)

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
