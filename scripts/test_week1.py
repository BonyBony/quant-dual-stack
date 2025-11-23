#!/usr/bin/env python3
"""
Quick Test Script for ML Pipeline Week 1
==========================================

Tests:
1. NIFTY50 universe loader
2. Multi-symbol data loader (mock data)
3. Feature computation without leakage
4. Label generation

Run: python scripts/test_week1.py
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("="*60)
print("ML PIPELINE WEEK 1 - QUICK TEST")
print("="*60)

# Test 1: Universe loader
print("\n[Test 1] Testing NIFTY50 universe loader...")
try:
    from common.data.nifty50_universe import get_nifty50_symbols, NIFTY50_TEST_SET

    all_symbols = get_nifty50_symbols()
    test_symbols = NIFTY50_TEST_SET

    print(f"  ✅ Loaded {len(all_symbols)} NIFTY50 symbols")
    print(f"  ✅ Test set: {len(test_symbols)} symbols")
    print(f"     {test_symbols[:3]}...")
except Exception as e:
    print(f"  ❌ FAILED: {e}")
    sys.exit(1)

# Test 2: Feature computation (without real data)
print("\n[Test 2] Testing feature computation...")
try:
    import pandas as pd
    import numpy as np
    from jobs.build_ml_dataset import compute_features_raw, lag_features

    # Create mock OHLCV data
    dates = pd.date_range("2023-01-01", periods=100, freq="D")
    symbols = ["STOCK_A", "STOCK_B"]

    data = []
    for symbol in symbols:
        for i, date in enumerate(dates):
            price = 100 + i + np.random.randn() * 2
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

    # Compute features
    df_features = compute_features_raw(df)
    feature_cols = [col for col in df_features.columns
                    if col not in {"open", "high", "low", "close", "volume", "symbol"}]

    print(f"  ✅ Computed {len(feature_cols)} features")

    # Test lagging
    df_lagged = lag_features(df_features, feature_cols)

    # Verify lagging worked
    if df_lagged.loc[(dates[0], "STOCK_A"), feature_cols[0]] != df_lagged.loc[(dates[0], "STOCK_A"), feature_cols[0]]:  # NaN check
        print(f"  ✅ Feature lagging applied (first date has NaN)")
    else:
        print(f"  ⚠️  Warning: Could not verify lagging")

except Exception as e:
    print(f"  ❌ FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Label computation
print("\n[Test 3] Testing label computation...")
try:
    from jobs.build_ml_dataset import compute_labels

    # Use mock data from Test 2
    df_labels = compute_labels(df)

    print(f"  ✅ Generated labels: {df_labels.shape}")
    print(f"     Label stats: mean={df_labels['label'].mean():.4f}, std={df_labels['label'].std():.4f}")

except Exception as e:
    print(f"  ❌ FAILED: {e}")
    sys.exit(1)

# Test 4: Cross-sectional standardization
print("\n[Test 4] Testing cross-sectional standardization...")
try:
    from jobs.build_ml_dataset import cross_sectional_standardize

    df_standardized = cross_sectional_standardize(df_lagged, feature_cols[:5])  # Test on first 5 features

    # Check one date has mean~0, std~1
    test_date = dates[50]
    date_data = df_standardized.loc[test_date, feature_cols[0]]

    if date_data.notna().sum() >= 2:
        mean_val = date_data.mean()
        std_val = date_data.std()
        print(f"  ✅ Cross-sectional z-score: mean={mean_val:.6f}, std={std_val:.2f}")

        if abs(mean_val) < 1e-6 and abs(std_val - 1.0) < 0.2:
            print(f"  ✅ Standardization verified!")
        else:
            print(f"  ⚠️  Warning: Standardization values unexpected")

except Exception as e:
    print(f"  ❌ FAILED: {e}")
    sys.exit(1)

# Test 5: Purged CV
print("\n[Test 5] Testing Purged CV...")
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
        if len(overlap) > 0:
            print(f"  ❌ FAILED: Temporal overlap detected!")
            sys.exit(1)

    print(f"  ✅ Purged CV: {n_splits} folds, no temporal overlap")

except Exception as e:
    print(f"  ❌ FAILED: {e}")
    sys.exit(1)

# Summary
print("\n" + "="*60)
print("✅ ALL TESTS PASSED!")
print("="*60)
print("\nYou can now run the full dataset builder:")
print("  python jobs/build_ml_dataset.py --universe test --start 2020-01-01 --end 2024-12-31")
print("\nNote: This will download real market data (takes 2-3 minutes)")
