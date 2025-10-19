"""Build leak-proof daily cross-sectional dataset for NIFTY equities."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
import yaml

from common.data.yf_loader import load_daily


# ---------------------------------------------------------------------------
# Feature helpers
# ---------------------------------------------------------------------------

def atr_series(df: pd.DataFrame, lookback: int = 14) -> pd.Series:
    high, low, close = df["high"], df["low"], df["close"]
    prev_close = close.shift(1)
    tr = pd.concat([
        (high - low),
        (high - prev_close).abs(),
        (low - prev_close).abs(),
    ], axis=1).max(axis=1)
    return tr.rolling(lookback).mean()


def bollinger_pct(close: pd.Series, window: int = 20) -> pd.Series:
    ma = close.rolling(window).mean()
    std = close.rolling(window).std(ddof=0)
    return (close - ma) / (2 * std)


def realised_vol(close: pd.Series, window: int = 20) -> pd.Series:
    log_ret = np.log(close / close.shift(1))
    return log_ret.rolling(window).std(ddof=0)


def prepare_universe(cfg: Dict) -> List[str]:
    if "universe" in cfg:
        return list(cfg["universe"])
    if "universe_file" in cfg:
        path = Path(cfg["universe_file"])
        if not path.exists():
            raise FileNotFoundError(path)
        symbols = [line.strip() for line in path.read_text().splitlines() if line.strip()]
        return symbols
    raise ValueError("Config must specify 'universe' or 'universe_file'.")


def download_panel(symbols: List[str], start: str, end: str, buffer_days: int = 200) -> pd.DataFrame:
    frames = []
    start_buffer = (pd.Timestamp(start) - pd.Timedelta(days=buffer_days)).date().isoformat()
    for sym in symbols:
        try:
            df = load_daily(sym, start_buffer, end)
        except Exception as exc:  # pragma: no cover - network handling
            print(f"[WARN] failed to load {sym}: {exc}")
            continue
        df = df.reset_index()
        df.rename(columns={df.columns[0]: "date"}, inplace=True)
        df["symbol"] = sym
        frames.append(df)
    if not frames:
        raise RuntimeError("No data downloaded for any symbols.")

    panel = pd.concat(frames, ignore_index=True)
    panel["date"] = pd.to_datetime(panel["date"]).dt.tz_localize(None)
    panel = panel.sort_values(["date", "symbol"])\
                 [["date", "symbol", "open", "high", "low", "close", "volume"]]
    panel = panel.loc[panel["date"] >= pd.Timestamp(start)]
    panel = panel.drop_duplicates(subset=["date", "symbol"])
    return panel.reset_index(drop=True)


def add_features(panel: pd.DataFrame) -> pd.DataFrame:
    panel = panel.copy()
    panel_group = panel.groupby("symbol", group_keys=False)

    panel["ret_1d"] = panel_group["close"].apply(lambda s: np.log(s / s.shift(1)))
    panel["ret_5d"] = panel_group["close"].apply(lambda s: np.log(s / s.shift(5)))
    panel["volume_ratio"] = panel_group["volume"].apply(lambda s: s / s.rolling(20).mean())
    panel["range_ratio"] = panel_group.apply(lambda g: (g["high"] - g["low"]) / g["close"])
    panel["atr_14"] = panel_group.apply(lambda g: atr_series(g, 14))
    panel["atr_norm"] = panel["atr_14"] / panel["close"]
    panel["bb_pct"] = panel_group["close"].apply(lambda s: bollinger_pct(s, 20))
    panel["realised_vol_20"] = panel_group["close"].apply(lambda s: realised_vol(s, 20))

    return panel


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
    panel = panel.copy()
    panel[feature_cols] = (
        panel.groupby("date")[feature_cols]
        .transform(lambda df: (df - df.mean()) / (df.std(ddof=0) + 1e-9))
    )
    return panel


def write_outputs(panel: pd.DataFrame, feature_cols: List[str], label_cols: List[str], cfg: Dict) -> None:
    features_path = Path(cfg["outputs"]["features"])
    labels_path = Path(cfg["outputs"]["labels"])
    meta_path = Path(cfg["outputs"].get("meta", "data/meta.json"))

    features_path.parent.mkdir(parents=True, exist_ok=True)
    labels_path.parent.mkdir(parents=True, exist_ok=True)
    meta_path.parent.mkdir(parents=True, exist_ok=True)

    feature_df = panel[["date", "symbol", *feature_cols]].dropna()
    feature_df.set_index(["date", "symbol"], inplace=True)
    feature_df.to_parquet(features_path)

    label_df = panel[["date", "symbol", *label_cols]].dropna()
    label_df.set_index(["date", "symbol"], inplace=True)
    label_df.to_parquet(labels_path)

    summary = {
        "symbols": sorted(panel["symbol"].unique()),
        "feature_columns": feature_cols,
        "label_columns": label_cols,
        "start": str(feature_df.index.get_level_values(0).min().date()),
        "end": str(feature_df.index.get_level_values(0).max().date()),
        "rows": int(len(feature_df)),
    }
    meta_path.write_text(json.dumps(summary, indent=2, default=str))

    print("Features saved to", features_path)
    print("Labels saved to", labels_path)
    print(json.dumps(summary, indent=2))


def main(config_path: Path) -> None:
    with open(config_path, "r") as fh:
        cfg = yaml.safe_load(fh)

    universe = prepare_universe(cfg)
    print(f"Universe size: {len(universe)}")

    start = cfg["start_date"]
    end = cfg.get("end_date") or pd.Timestamp.today().date().isoformat()

    panel = download_panel(universe, start, end, buffer_days=cfg.get("buffer_days", 200))
    panel = add_features(panel)
    panel = add_labels(panel)

    feature_cols = [
        "ret_1d",
        "ret_5d",
        "volume_ratio",
        "range_ratio",
        "atr_norm",
        "bb_pct",
        "realised_vol_20",
    ]
    label_cols = ["ret_fwd_1", "ret_fwd_sign"]

    panel = lag_features(panel, feature_cols)
    panel = panel.dropna(subset=feature_cols + label_cols)
    panel = cross_sectional_standardise(panel, feature_cols)

    write_outputs(panel, feature_cols, label_cols, cfg)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build cross-sectional ML dataset")
    parser.add_argument("--config", required=True, help="Path to dataset config YAML")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(Path(args.config))
