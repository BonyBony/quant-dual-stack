#!/usr/bin/env python3
"""
Simplified Week 1 Test - No External Dependencies Required
===========================================================

Tests core functionality without downloading real market data.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("="*60)
print("ML PIPELINE WEEK 1 - SIMPLIFIED TEST")
print("="*60)

# Test 1: Universe loader
print("\n[Test 1] Testing NIFTY50 universe loader...")
try:
    from common.data.nifty50_universe import get_nifty50_symbols, NIFTY50_TEST_SET

    all_symbols = get_nifty50_symbols()
    test_symbols = NIFTY50_TEST_SET

    print(f"  ✅ Loaded {len(all_symbols)} NIFTY50 symbols")
    print(f"  ✅ Test set: {test_symbols}")

    assert len(all_symbols) > 40, "Should have ~50 symbols"
    assert len(test_symbols) == 5, "Test set should have 5 symbols"
    assert "HDFCBANK.NS" in test_symbols, "HDFCBANK should be in test set"

except Exception as e:
    print(f"  ❌ FAILED: {e}")
    sys.exit(1)

# Test 2: Feature computation (mock data)
print("\n[Test 2] Testing feature computation with mock data...")
try:
    import pandas as pd
    import numpy as np

    # Create mock OHLCV data
    dates = pd.date_range("2023-01-01", periods=100, freq="D")
    symbols = ["STOCK_A", "STOCK_B"]

    data = []
    np.random.seed(42)  # Reproducible
    for symbol in symbols:
        base = 100 if symbol == "STOCK_A" else 200
        for i, date in enumerate(dates):
            price = base + i + np.random.randn() * 2
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

    print(f"  ✅ Created mock data: {df.shape}")
    assert df.shape == (200, 5), "Should have 200 rows, 5 columns"

except Exception as e:
    print(f"  ❌ FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Feature lagging (the most critical test!)
print("\n[Test 3] Testing feature lagging (prevents lookahead bias)...")
try:
    from jobs.build_ml_dataset import lag_features

    # Create simple feature
    df_test = df.copy()
    df_test['simple_feature'] = df_test.groupby('symbol')['close'].pct_change()

    # Lag it
    df_lagged = lag_features(df_test, ['simple_feature'])

    # Verify: first date should have NaN after lagging
    first_date = dates[0]
    for symbol in symbols:
        value = df_lagged.loc[(first_date, symbol), 'simple_feature']
        assert pd.isna(value), f"First date should have NaN for {symbol}"

    # Verify: lagged feature at T should equal raw feature at T-1
    for i in range(1, min(10, len(dates))):
        date_t = dates[i]
        date_t_minus_1 = dates[i - 1]

        for symbol in symbols:
            raw_at_t_minus_1 = df_test.loc[(date_t_minus_1, symbol), 'simple_feature']
            lagged_at_t = df_lagged.loc[(date_t, symbol), 'simple_feature']

            if not pd.isna(raw_at_t_minus_1) and not pd.isna(lagged_at_t):
                assert np.isclose(raw_at_t_minus_1, lagged_at_t, rtol=1e-5), \
                    f"Lagging failed for {symbol} at {date_t}"

    print(f"  ✅ Feature lagging works correctly!")
    print(f"     - First date has NaN (no previous data)")
    print(f"     - Lagged features use T-1 data at time T")

except Exception as e:
    print(f"  ❌ FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Cross-sectional standardization
print("\n[Test 4] Testing cross-sectional standardization...")
try:
    from jobs.build_ml_dataset import cross_sectional_standardize

    # Add a feature that varies across stocks
    df_test = df.copy()
    df_test['test_feature'] = df_test.groupby('symbol')['close'].transform(lambda x: x.pct_change())

    # Standardize cross-sectionally
    df_std = cross_sectional_standardize(df_test, ['test_feature'])

    # Check one date: mean should be ~0, std should be ~1
    test_date = dates[50]
    date_data = df_std.loc[test_date, 'test_feature']

    if date_data.notna().sum() >= 2:
        mean_val = date_data.mean()
        std_val = date_data.std()

        print(f"  ✅ Cross-sectional z-score at {test_date}:")
        print(f"     - Mean: {mean_val:.6f} (should be ~0)")
        print(f"     - Std:  {std_val:.2f} (should be ~1)")

        assert abs(mean_val) < 1e-6, "Mean should be close to 0"
        assert abs(std_val - 1.0) < 0.2, "Std should be close to 1"

except Exception as e:
    print(f"  ❌ FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Label computation
print("\n[Test 5] Testing label computation...")
try:
    from jobs.build_ml_dataset import compute_labels

    df_labels = compute_labels(df)

    print(f"  ✅ Generated labels: {df_labels.shape}")
    print(f"     - Columns: {list(df_labels.columns)}")
    print(f"     - Label stats: mean={df_labels['label'].mean():.4f}, std={df_labels['label'].std():.4f}")

    # Check last date has NaN (no future data)
    last_date = dates[-1]
    for symbol in symbols:
        label_val = df_labels.loc[(last_date, symbol), 'label']
        assert pd.isna(label_val), f"Last date should have NaN label for {symbol}"

except Exception as e:
    print(f"  ❌ FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 6: Purged CV
print("\n[Test 6] Testing Purged CV (time-series cross-validation)...")
try:
    from common.validation.purged_cv import PurgedGroupTimeSeriesSplit

    X = pd.DataFrame({"dummy": range(100)})
    groups = dates[:100]

    cv = PurgedGroupTimeSeriesSplit(n_splits=5, embargo_groups=5)
    n_splits = 0

    for train_idx, test_idx in cv.split(X, groups=groups):
        n_splits += 1
        train_dates = set(dates[train_idx])
        test_dates = set(dates[test_idx])

        # Check no overlap
        overlap = train_dates.intersection(test_dates)
        assert len(overlap) == 0, f"Fold {n_splits}: Temporal overlap detected!"

        # Check train comes before test
        if train_dates and test_dates:
            max_train = max(train_dates)
            min_test = min(test_dates)
            assert max_train < min_test, f"Fold {n_splits}: Train not before test!"

    print(f"  ✅ Purged CV: {n_splits} folds")
    print(f"     - No temporal overlap between train/test")
    print(f"     - Train dates strictly before test dates")

except Exception as e:
    print(f"  ❌ FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Summary
print("\n" + "="*60)
print("✅ ALL TESTS PASSED!")
print("="*60)
print("\nCore ML infrastructure is working correctly:")
print("  ✓ Universe loader")
print("  ✓ Feature lagging (no lookahead bias)")
print("  ✓ Cross-sectional standardization")
print("  ✓ Label generation")
print("  ✓ Purged time-series CV")
print("\nNext steps:")
print("  1. Install yfinance: pip3 install --user yfinance")
print("  2. Run full dataset builder:")
print("     python3 jobs/build_ml_dataset.py --universe test --start 2020-01-01 --end 2024-12-31")
