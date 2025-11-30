"""Build leak-proof daily cross-sectional dataset with configurable features."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import yaml
from ta.trend import ADXIndicator, EMAIndicator, MACD
from ta.momentum import RSIIndicator

from common.data.yf_loader import load_daily


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def prepare_universe(cfg: Dict) -> List[str]:
    if "universe" in cfg:
        return list(cfg["universe"])
    if "universe_file" in cfg:
        path = Path(cfg["universe_file"])
        if not path.exists():
            raise FileNotFoundError(path)
        return [line.strip() for line in path.read_text().splitlines() if line.strip()]
    raise ValueError("Universe not specified in config")


def download_panel(symbols: List[str], start: str, end: str, buffer_days: int) -> pd.DataFrame:
    frames = []
    start_buffer = (pd.Timestamp(start) - pd.Timedelta(days=buffer_days)).date().isoformat()
    for sym in symbols:
        try:
            df = load_daily(sym, start_buffer, end)
        except Exception as exc:  # pragma: no cover
            print(f"[WARN] failed to load {sym}: {exc}")
            continue
        df = df.reset_index()
        df.rename(columns={df.columns[0]: "date"}, inplace=True)
        df["symbol"] = sym
        frames.append(df[["date", "symbol", "open", "high", "low", "close", "volume"]])
    if not frames:
        raise RuntimeError("No data downloaded")
    panel = pd.concat(frames, ignore_index=True)
    panel["date"] = pd.to_datetime(panel["date"]).dt.tz_localize(None)
    panel = panel.sort_values(["date", "symbol"]).drop_duplicates(subset=["date", "symbol"])
    panel = panel.loc[panel["date"] >= pd.Timestamp(start)]
    return panel.reset_index(drop=True)


def ema_slope(series: pd.Series, window: int, slope_window: int = 1) -> pd.Series:
    ema = EMAIndicator(close=series, window=window, fillna=True).ema_indicator()
    return ema - ema.shift(slope_window)


def macd_features(close: pd.Series, params: Dict) -> Dict[str, pd.Series]:
    macd = MACD(close=close, **params, fillna=True)
    return {
        "macd": macd.macd(),
        "macd_signal": macd.macd_signal(),
        "macd_hist": macd.macd_diff(),
    }


def ppo_features(close: pd.Series, params: Dict) -> Dict[str, pd.Series]:
    fast = params.get("window_fast", 12)
    slow = params.get("window_slow", 26)
    signal = params.get("window_sign", 9)
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    ppo = (ema_fast - ema_slow) / ema_slow.replace(0, np.nan)
    ppo_signal = ppo.ewm(span=signal, adjust=False).mean()
    ppo_hist = ppo - ppo_signal
    return {"ppo": ppo, "ppo_signal": ppo_signal, "ppo_hist": ppo_hist}


def adx_feature(high: pd.Series, low: pd.Series, close: pd.Series, window: int) -> pd.Series:
    adx = ADXIndicator(high=high, low=low, close=close, window=window, fillna=True)
    return adx.adx()


def money_flow_index(high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series, window: int) -> pd.Series:
    typical_price = (high + low + close) / 3
    raw_flow = typical_price * volume.fillna(0)
    direction = np.sign(typical_price.diff())
    positive = raw_flow.where(direction > 0, 0.0)
    negative = raw_flow.where(direction < 0, 0.0)
    pos_flow = positive.rolling(window).sum()
    neg_flow = negative.rolling(window).sum().replace(0.0, np.nan)
    mfi = 100 - (100 / (1 + pos_flow / neg_flow))
    return mfi


def obv_indicator(close: pd.Series, volume: pd.Series) -> pd.Series:
    direction = np.sign(close.diff()).fillna(0)
    obv = (direction * volume.fillna(0)).cumsum()
    return obv


def realise_vol(close: pd.Series, window: int) -> pd.Series:
    log_ret = np.log(close / close.shift(1))
    return log_ret.rolling(window).std(ddof=0)


def bollinger_pct(close: pd.Series, window: int) -> pd.Series:
    ma = close.rolling(window).mean()
    std = close.rolling(window).std(ddof=0)
    return (close - ma) / (2 * std)


def atr_series(high: pd.Series, low: pd.Series, close: pd.Series, window: int) -> pd.Series:
    prev_close = close.shift(1)
    tr = pd.concat([(high - low), (high - prev_close).abs(), (low - prev_close).abs()], axis=1).max(axis=1)
    return tr.rolling(window).mean()


def add_weekly_features(group: pd.DataFrame, cfg: Dict) -> Dict[str, pd.Series]:
    weekly = group.set_index("date").resample("W-FRI").last()
    weekly_features: Dict[str, pd.Series] = {}
    if cfg.get("weekly_macd", {}).get("enabled", True):
        params = cfg["weekly_macd"].get("params", {"window_fast": 12, "window_slow": 26, "window_sign": 9})
        hist = MACD(close=weekly["close"], fillna=True, **params).macd_diff()
        weekly_features["weekly_macd_hist"] = hist.reindex(group["date"]).ffill()
    if cfg.get("weekly_rsi", {}).get("enabled", True):
        window = cfg["weekly_rsi"].get("window", 14)
        rsi = RSIIndicator(close=weekly["close"], window=window, fillna=True).rsi()
        weekly_features["weekly_rsi"] = rsi.reindex(group["date"]).ffill()
    return weekly_features


def compute_features(panel: pd.DataFrame, feature_cfg: Dict) -> Tuple[pd.DataFrame, List[str]]:
    panel = panel.copy()
    feature_cols: List[str] = []
    grouped = panel.groupby("symbol", group_keys=False)

    def assign_feature(name: str, series: pd.Series) -> None:
        panel[name] = series
        feature_cols.append(name)

    for sym, group in grouped:
        close = group["close"]
        high, low, open_ = group["high"], group["low"], group["open"]
        volume = group["volume"].replace(0, np.nan)

        if feature_cfg["trend"].get("enabled", True):
            macd_feats = macd_features(close, feature_cfg["trend"].get("macd", {"window_fast": 12, "window_slow": 26, "window_sign": 9}))
            for name, series in macd_feats.items():
                assign_feature(f"{name}", series)
            ppo_feats = ppo_features(close, feature_cfg["trend"].get("ppo", {"window_fast": 12, "window_slow": 26, "window_sign": 9}))
            for name, series in ppo_feats.items():
                assign_feature(f"{name}", series)
            for window in feature_cfg["trend"].get("ema_windows", [10, 20, 50]):
                assign_feature(f"ema_slope_{window}", ema_slope(close, window))
            assign_feature("adx", adx_feature(high, low, close, feature_cfg["trend"].get("adx_window", 14)))

        if feature_cfg["mean_reversion"].get("enabled", True):
            window_rsi = feature_cfg["mean_reversion"].get("rsi_window", 14)
            assign_feature("rsi", RSIIndicator(close=close, window=window_rsi, fillna=True).rsi())
            window_ret = feature_cfg["mean_reversion"].get("return_z_window", 20)
            ret = np.log(close / close.shift(1))
            assign_feature("return_zscore", (ret - ret.rolling(window_ret).mean()) / (ret.rolling(window_ret).std(ddof=0) + 1e-9))
            window_boll = feature_cfg["mean_reversion"].get("bollinger_window", 20)
            assign_feature("bollinger_pct", bollinger_pct(close, window_boll))

        if feature_cfg["volatility"].get("enabled", True):
            window_atr = feature_cfg["volatility"].get("atr_window", 14)
            atr = atr_series(high, low, close, window_atr)
            assign_feature("atr", atr)
            assign_feature("atr_norm", atr / close)
            window_rvol = feature_cfg["volatility"].get("realised_vol_window", 20)
            assign_feature("realised_vol", realise_vol(close, window_rvol))

        if feature_cfg["volume_flow"].get("enabled", True):
            window_vol = feature_cfg["volume_flow"].get("volume_window", 20)
            assign_feature("volume_zscore", (volume - volume.rolling(window_vol).mean()) / (volume.rolling(window_vol).std(ddof=0) + 1e-9))
            window_mfi = feature_cfg["volume_flow"].get("mfi_window", 14)
            assign_feature("mfi", money_flow_index(high, low, close, volume.fillna(0), window_mfi))
            assign_feature("obv", obv_indicator(close, volume.fillna(0)))

        if feature_cfg["microstructure"].get("enabled", True):
            assign_feature("gap_pct", open_ / close.shift(1) - 1)
            assign_feature("overnight_ret", np.log(open_ / close.shift(1)))
            assign_feature("intraday_ret", np.log(close / open_))

        if feature_cfg["regime"].get("enabled", True):
            weekly_feats = add_weekly_features(group, feature_cfg["regime"])
            for name, series in weekly_feats.items():
                assign_feature(name, series)

    feature_cols = list(dict.fromkeys(feature_cols))  # deduplicate while preserving order
    return panel, feature_cols


def add_labels(panel: pd.DataFrame) -> pd.DataFrame:
    panel = panel.copy()
    group = panel.groupby("symbol", group_keys=False)
    panel["ret_fwd_1"] = group["close"].apply(lambda s: np.log(s.shift(-1) / s))
    panel["ret_fwd_sign"] = np.sign(panel["ret_fwd_1"])
    return panel


def lag_features(panel: pd.DataFrame, feature_cols: List[str]) -> pd.DataFrame:
    panel = panel.copy()
    group = panel.groupby("symbol", group_keys=False)
    for col in feature_cols:
        panel[col] = group[col].apply(lambda s: s.shift(1))
    return panel


def cross_sectional_standardise(panel: pd.DataFrame, feature_cols: List[str]) -> pd.DataFrame:
    if not feature_cols:
        return panel
    if panel.empty:
        raise RuntimeError("No rows available for standardisation")
    panel = panel.copy()
    panel[feature_cols] = panel.groupby("date")[feature_cols].transform(
        lambda df: (df - df.mean()) / (df.std(ddof=0) + 1e-9)
    )
    return panel


def save_outputs(panel: pd.DataFrame, feature_cols: List[str], cfg: Dict) -> None:
    features_path = Path(cfg["outputs"]["features"])
    labels_path = Path(cfg["outputs"]["labels"])
    meta_path = Path(cfg["outputs"].get("meta", "data/meta.json"))
    corr_path = Path(cfg["outputs"].get("corr_png", "data/feature_corr.png"))

    features_path.parent.mkdir(parents=True, exist_ok=True)
    labels_path.parent.mkdir(parents=True, exist_ok=True)
    meta_path.parent.mkdir(parents=True, exist_ok=True)
    corr_path.parent.mkdir(parents=True, exist_ok=True)

    feature_df = panel[["date", "symbol", *feature_cols]].dropna()
    feature_df.set_index(["date", "symbol"], inplace=True)
    feature_df.to_parquet(features_path)

    label_cols = ["ret_fwd_1", "ret_fwd_sign"]
    label_df = panel[["date", "symbol", *label_cols]].dropna()
    label_df.set_index(["date", "symbol"], inplace=True)
    label_df.to_parquet(labels_path)

    meta = {
        "symbols": sorted(panel["symbol"].unique()),
        "feature_columns": feature_cols,
        "label_columns": label_cols,
        "start": str(feature_df.index.get_level_values(0).min().date()),
        "end": str(feature_df.index.get_level_values(0).max().date()),
        "rows": int(len(feature_df)),
    }
    meta_path.write_text(json.dumps(meta, indent=2, default=str))

    # correlation heatmap
    corr = feature_df.reset_index(drop=True)[feature_cols].corr()
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(0.6 * len(feature_cols), 0.6 * len(feature_cols)))
    im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(len(feature_cols)))
    ax.set_xticklabels(feature_cols, rotation=90)
    ax.set_yticks(range(len(feature_cols)))
    ax.set_yticklabels(feature_cols)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(corr_path, dpi=150)
    plt.close(fig)

    print(json.dumps(meta, indent=2))
    print("Features saved to", features_path)
    print("Labels saved to", labels_path)
    print("Correlation heatmap saved to", corr_path)


def load_feature_config(path: Path | None) -> Dict:
    default_cfg = {
        "trend": {
            "enabled": True,
            "macd": {"window_fast": 12, "window_slow": 26, "window_sign": 9},
            "ppo": {"window_fast": 12, "window_slow": 26, "window_sign": 9},
            "ema_windows": [10, 20, 50],
            "adx_window": 14,
        },
        "mean_reversion": {"enabled": True, "rsi_window": 14, "return_z_window": 20, "bollinger_window": 20},
        "volatility": {"enabled": True, "atr_window": 14, "realised_vol_window": 20},
        "volume_flow": {"enabled": True, "volume_window": 20, "mfi_window": 14},
        "microstructure": {"enabled": True},
        "regime": {
            "enabled": True,
            "weekly_macd": {"enabled": True, "params": {"window_fast": 12, "window_slow": 26, "window_sign": 9}},
            "weekly_rsi": {"enabled": True, "window": 14},
        },
    }
    if path is None or not path.exists():
        return default_cfg
    with open(path, "r") as fh:
        user_cfg = yaml.safe_load(fh)
    # deep merge defaults with user cfg
    cfg = default_cfg
    for block, block_cfg in user_cfg.items():
        cfg.setdefault(block, {}).update(block_cfg)
    return cfg


def main(args: argparse.Namespace) -> None:
    cfg_path = Path(args.config)
    with open(cfg_path, "r") as fh:
        cfg = yaml.safe_load(fh)

    feature_cfg = load_feature_config(Path(args.feature_config) if args.feature_config else Path(cfg.get("feature_config", "")))

    universe = prepare_universe(cfg)
    print(f"Universe size: {len(universe)}")

    start = cfg["start_date"]
    end = cfg.get("end_date") or pd.Timestamp.today().date().isoformat()
    panel = download_panel(universe, start, end, buffer_days=cfg.get("buffer_days", 200))

    panel, feature_cols = compute_features(panel, feature_cfg)
    panel = add_labels(panel)
    panel = lag_features(panel, feature_cols)
    panel = panel.dropna(subset=feature_cols + ["ret_fwd_1", "ret_fwd_sign"])
    if panel.empty:
        raise RuntimeError("Dataset empty after lag/dropna; check feature configuration")
    panel = cross_sectional_standardise(panel, feature_cols)

    save_outputs(panel, feature_cols, cfg)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build cross-sectional ML dataset")
    parser.add_argument("--config", required=True, help="Dataset configuration YAML")
    parser.add_argument("--feature-config", default=None, help="Feature configuration YAML")
    return parser.parse_args()


if __name__ == "__main__":
    main(parse_args())
