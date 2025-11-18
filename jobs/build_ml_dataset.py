"""
Build Leak-Proof ML Dataset for Cross-Sectional Return Prediction
==================================================================

Creates features.parquet and labels.parquet with:
  1. Proper feature lagging (shift by 1 day) - NO FUTURE LEAK!
  2. Cross-sectional standardization (z-score per day across stocks)
  3. Universe: NIFTY50 (or custom list)
  4. Label: next-day log return

Usage
-----
  python jobs/build_ml_dataset.py --start 2020-01-01 --end 2024-12-31 --universe nifty50

Critical Rules (NO EXCEPTIONS!)
--------------------------------
  1. ALL features must be lagged by at least 1 day (.shift(1))
  2. Cross-sectional standardization ONLY uses data from that day
  3. Labels computed from future returns (but never used as features!)
  4. Check for NaN leakage after lagging

Output
------
  data/features.parquet: (date, symbol) index with lagged, z-scored features
  data/labels.parquet: (date, symbol) index with forward returns
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import numpy as np
import pandas as pd

from common.data.nifty50_universe import get_nifty50_symbols, NIFTY50_TEST_SET
from common.data.yf_loader import load_daily_multi


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


# ================================================================
# FEATURE COMPUTATION (all must be lagged later!)
# ================================================================

def compute_features_raw(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute raw features from OHLCV data (NOT YET LAGGED).

    These features use data up to and including time t.
    We'll lag them by 1 day later to make them valid for predicting t+1.

    Features included:
    - Price momentum (returns over multiple horizons)
    - Volatility (realized vol, ATR)
    - Volume indicators (volume z-score, MFI)
    - Trend (MACD, RSI, moving average ratios)

    Parameters
    ----------
    df : pd.DataFrame
        Must have index=(date, symbol) and columns=[open, high, low, close, volume]

    Returns
    -------
    pd.DataFrame
        Same index as df, with additional feature columns (NOT lagged yet!)
    """
    df = df.copy()

    # ==================== PRICE MOMENTUM ====================
    # Returns over multiple lookback periods
    for lookback in [1, 5, 10, 20, 60, 120]:
        df[f"ret_{lookback}d"] = df.groupby("symbol")["close"].pct_change(lookback)

    # Log returns (more stable for ML)
    for lookback in [5, 20, 60]:
        df[f"log_ret_{lookback}d"] = df.groupby("symbol")["close"].transform(
            lambda x: np.log(x / x.shift(lookback))
        )

    # ==================== VOLATILITY ====================
    # Realized volatility (std of returns)
    for window in [10, 20, 60]:
        df[f"vol_{window}d"] = df.groupby("symbol")["ret_1d"].transform(
            lambda x: x.rolling(window).std()
        )

    # ATR (Average True Range)
    def _compute_atr(group, window=14):
        high = group["high"]
        low = group["low"]
        close = group["close"]
        prev_close = close.shift(1)

        tr = pd.concat([
            high - low,
            (high - prev_close).abs(),
            (low - prev_close).abs()
        ], axis=1).max(axis=1)

        atr = tr.rolling(window).mean()
        # Normalize by price
        atr_pct = atr / close
        return atr_pct

    for window in [14, 30]:
        df[f"atr_{window}d"] = df.groupby("symbol", group_keys=False).apply(
            lambda g: _compute_atr(g, window)
        )

    # ==================== VOLUME ====================
    # Volume z-score (cross-sectional per stock)
    for window in [20, 60]:
        df[f"volume_zscore_{window}d"] = df.groupby("symbol")["volume"].transform(
            lambda x: (x - x.rolling(window).mean()) / (x.rolling(window).std() + 1e-9)
        )

    # Volume ratio (today vs moving average)
    for window in [20, 60]:
        df[f"volume_ratio_{window}d"] = df.groupby("symbol")["volume"].transform(
            lambda x: x / (x.rolling(window).mean() + 1e-9)
        )

    # Money Flow Index (MFI)
    def _compute_mfi(group, window=14):
        if not {"high", "low", "close", "volume"}.issubset(group.columns):
            return pd.Series(np.nan, index=group.index)

        high = group["high"]
        low = group["low"]
        close = group["close"]
        volume = group["volume"]

        typical_price = (high + low + close) / 3
        money_flow = typical_price * volume

        positive_flow = money_flow.where(typical_price > typical_price.shift(1), 0.0)
        negative_flow = money_flow.where(typical_price < typical_price.shift(1), 0.0)

        positive_sum = positive_flow.rolling(window).sum()
        negative_sum = negative_flow.rolling(window).sum()

        mfi = 100 - (100 / (1 + positive_sum / (negative_sum + 1e-9)))
        return mfi

    df["mfi_14d"] = df.groupby("symbol", group_keys=False).apply(
        lambda g: _compute_mfi(g, 14)
    )

    # ==================== TREND ====================
    # MACD components
    for fast, slow, signal in [(12, 26, 9), (8, 21, 5)]:
        close_gb = df.groupby("symbol")["close"]
        macd_line = close_gb.transform(lambda x: x.ewm(span=fast, adjust=False).mean()) - \
                    close_gb.transform(lambda x: x.ewm(span=slow, adjust=False).mean())
        signal_line = macd_line.groupby(df["symbol"]).transform(
            lambda x: x.ewm(span=signal, adjust=False).mean()
        )
        histogram = macd_line - signal_line

        # Normalize by price to make cross-sectional comparable
        df[f"macd_{fast}_{slow}"] = macd_line / df["close"]
        df[f"macd_signal_{fast}_{slow}_{signal}"] = signal_line / df["close"]
        df[f"macd_hist_{fast}_{slow}_{signal}"] = histogram / df["close"]

    # RSI (Relative Strength Index)
    def _compute_rsi(series, length=14):
        delta = series.diff()
        gain = delta.clip(lower=0).ewm(alpha=1/length, adjust=False, min_periods=length).mean()
        loss = -delta.clip(upper=0).ewm(alpha=1/length, adjust=False, min_periods=length).mean()
        rs = gain / (loss + 1e-9)
        rsi = 100 - (100 / (1 + rs))
        return rsi

    df["rsi_14d"] = df.groupby("symbol")["close"].transform(lambda x: _compute_rsi(x, 14))

    # Moving average ratios
    for window in [20, 50, 200]:
        df[f"ma_ratio_{window}d"] = df.groupby("symbol")["close"].transform(
            lambda x: x / (x.rolling(window).mean() + 1e-9)
        )

    # ==================== MICROSTRUCTURE ====================
    # Gap % (open vs previous close)
    df["gap_pct"] = df.groupby("symbol").apply(
        lambda g: (g["open"] - g["close"].shift(1)) / (g["close"].shift(1) + 1e-9)
    )

    # Overnight return (close to next open)
    df["overnight_ret"] = df.groupby("symbol").apply(
        lambda g: (g["open"] - g["close"].shift(1)) / (g["close"].shift(1) + 1e-9)
    )

    # Intraday return (open to close)
    df["intraday_ret"] = (df["close"] - df["open"]) / (df["open"] + 1e-9)

    # High-low range as % of close
    df["hl_range_pct"] = (df["high"] - df["low"]) / (df["close"] + 1e-9)

    return df


# ================================================================
# LAG FEATURES (CRITICAL!)
# ================================================================

def lag_features(df: pd.DataFrame, feature_cols: list[str]) -> pd.DataFrame:
    """
    Lag all features by 1 day to prevent lookahead bias.

    This is THE MOST CRITICAL STEP for leak-proof ML!

    At time t, we can only use information available up to t-1.
    So all features computed at time t must be shifted forward by 1 day.

    Parameters
    ----------
    df : pd.DataFrame
        Index=(date, symbol), columns include features
    feature_cols : list[str]
        Names of feature columns to lag

    Returns
    -------
    pd.DataFrame
        Same structure, but features are now lagged by 1 day
    """
    df = df.copy()

    for col in feature_cols:
        if col in df.columns:
            # Lag by 1 day WITHIN each symbol
            df[col] = df.groupby("symbol")[col].shift(1)

    return df


# ================================================================
# CROSS-SECTIONAL STANDARDIZATION
# ================================================================

def cross_sectional_standardize(df: pd.DataFrame, feature_cols: list[str]) -> pd.DataFrame:
    """
    Z-score features cross-sectionally (across stocks) for each date.

    This ensures features are comparable across stocks and reduces
    the impact of market-wide regimes.

    For each date, compute: z_i = (x_i - mean(x_all)) / std(x_all)

    Parameters
    ----------
    df : pd.DataFrame
        Index=(date, symbol), columns include features
    feature_cols : list[str]
        Names of feature columns to standardize

    Returns
    -------
    pd.DataFrame
        Same structure, but features are cross-sectionally z-scored
    """
    df = df.copy()

    # Reset index to access 'date' as column
    df_reset = df.reset_index()

    for col in feature_cols:
        if col in df_reset.columns:
            # Z-score within each date (across symbols)
            df_reset[col] = df_reset.groupby("date")[col].transform(
                lambda x: (x - x.mean()) / (x.std(ddof=0) + 1e-9)
            )

    # Restore multi-index
    df_standardized = df_reset.set_index(["date", "symbol"])

    return df_standardized


# ================================================================
# LABEL COMPUTATION
# ================================================================

def compute_labels(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute forward-looking labels (next-day log returns).

    Label at time t = return from t to t+1.
    This is what we're trying to predict!

    Parameters
    ----------
    df : pd.DataFrame
        Index=(date, symbol), must have 'close' column

    Returns
    -------
    pd.DataFrame
        Index=(date, symbol), column='label' (next-day log return)
    """
    df = df.copy()

    # Next-day log return (what we're predicting)
    df["label"] = df.groupby("symbol")["close"].transform(
        lambda x: np.log(x.shift(-1) / x)
    )

    # Also compute classification label (sign of return)
    df["label_sign"] = np.sign(df["label"])

    # Winsorize extreme returns (cap at ±20% daily return)
    df["label"] = df["label"].clip(lower=-0.20, upper=0.20)

    return df[["label", "label_sign"]]


# ================================================================
# MAIN PIPELINE
# ================================================================

def main(args):
    logger.info("="*60)
    logger.info("ML DATASET BUILDER - LEAK-PROOF PIPELINE")
    logger.info("="*60)

    # ==================== LOAD DATA ====================
    logger.info(f"Loading universe: {args.universe}")

    if args.universe == "nifty50":
        symbols = get_nifty50_symbols()
    elif args.universe == "test":
        symbols = NIFTY50_TEST_SET
    else:
        symbols = args.symbols.split(",")

    logger.info(f"Symbols: {len(symbols)} stocks")
    logger.info(f"Date range: {args.start} to {args.end}")

    df_raw = load_daily_multi(symbols, args.start, args.end, max_workers=args.workers)

    if df_raw.empty:
        raise RuntimeError("No data loaded! Check symbols and date range.")

    logger.info(f"Loaded {len(df_raw)} rows from {len(df_raw.index.get_level_values('symbol').unique())} symbols")

    # ==================== COMPUTE RAW FEATURES ====================
    logger.info("Computing raw features (NOT lagged yet)...")
    df_features = compute_features_raw(df_raw)

    # Get list of feature columns (exclude OHLCV)
    base_cols = {"open", "high", "low", "close", "volume", "symbol"}
    feature_cols = [col for col in df_features.columns if col not in base_cols]
    logger.info(f"Computed {len(feature_cols)} raw features")

    # ==================== LAG FEATURES (CRITICAL!) ====================
    logger.info("Lagging features by 1 day (preventing lookahead bias)...")
    df_lagged = lag_features(df_features, feature_cols)

    # Check for NaN leakage
    nan_before = df_features[feature_cols].isna().sum().sum()
    nan_after = df_lagged[feature_cols].isna().sum().sum()
    logger.info(f"NaN counts - before lag: {nan_before}, after lag: {nan_after}")

    # ==================== CROSS-SECTIONAL STANDARDIZATION ====================
    logger.info("Cross-sectional standardization (z-score per date)...")
    df_standardized = cross_sectional_standardize(df_lagged, feature_cols)

    # ==================== COMPUTE LABELS ====================
    logger.info("Computing labels (next-day log returns)...")
    df_labels = compute_labels(df_raw)

    # ==================== ALIGN FEATURES & LABELS ====================
    # Both have same (date, symbol) index, so they're naturally aligned
    # Drop rows with NaN in features OR labels
    df_final_features = df_standardized[feature_cols].copy()
    df_final_labels = df_labels.copy()

    # Find common non-NaN indices
    features_valid = df_final_features.dropna(how="any")
    labels_valid = df_final_labels.dropna(how="any")

    common_index = features_valid.index.intersection(labels_valid.index)

    df_final_features = df_final_features.loc[common_index]
    df_final_labels = df_final_labels.loc[common_index]

    logger.info(f"Final dataset: {len(df_final_features)} rows (after dropping NaN)")
    logger.info(f"Date range: {df_final_features.index.get_level_values('date').min()} to {df_final_features.index.get_level_values('date').max()}")

    # ==================== SAVE TO DISK ====================
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    features_path = output_dir / "features.parquet"
    labels_path = output_dir / "labels.parquet"

    logger.info(f"Saving features to {features_path}")
    df_final_features.to_parquet(features_path)

    logger.info(f"Saving labels to {labels_path}")
    df_final_labels.to_parquet(labels_path)

    # ==================== VALIDATION REPORT ====================
    logger.info("="*60)
    logger.info("VALIDATION REPORT")
    logger.info("="*60)

    logger.info(f"Features shape: {df_final_features.shape}")
    logger.info(f"Labels shape: {df_final_labels.shape}")

    logger.info("\nLabel distribution:")
    logger.info(df_final_labels["label"].describe())

    logger.info("\nSample feature statistics:")
    logger.info(df_final_features.describe().T.head(10))

    # Check for leakage: correlation between features and labels should be weak
    sample_features = df_final_features.iloc[:, :5]  # First 5 features
    correlations = pd.DataFrame({
        "feature": sample_features.columns,
        "corr_with_label": [df_final_labels["label"].corr(sample_features[col]) for col in sample_features.columns]
    })
    logger.info("\nFeature-label correlations (should be small, <0.1 for first few):")
    logger.info(correlations)

    logger.info("="*60)
    logger.info("✅ DATASET BUILD COMPLETE!")
    logger.info("="*60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build leak-proof ML dataset")

    parser.add_argument("--start", default="2020-01-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", default="2024-12-31", help="End date (YYYY-MM-DD)")
    parser.add_argument("--universe", default="test", choices=["nifty50", "test", "custom"],
                        help="Stock universe (test=5 stocks, nifty50=all 50)")
    parser.add_argument("--symbols", default="", help="Comma-separated symbols (if universe=custom)")
    parser.add_argument("--output-dir", default="data", help="Output directory for parquet files")
    parser.add_argument("--workers", type=int, default=5, help="Parallel download workers")

    args = parser.parse_args()

    main(args)
