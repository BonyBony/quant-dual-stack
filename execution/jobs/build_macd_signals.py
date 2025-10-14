"""Build daily MACD trading signals based on selected parameters.

Workflow
--------
1. Load the latest parameter pick from `execution/cache/macd_params_*.json`.
2. Pull daily OHLCV data up to today (yfinance with NSE fallback).
3. Recompute the MACD histogram and deduce the latest strategy position.
4. Emit a one-row CSV under `execution/data/` describing the desired action
   (entry/exit/hold) along with the parameter tuple used.

This job is meant to run shortly after the selector job so the execution
layer (Backtrader or live broker interface) can ingest consistent signals.
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Dict, Iterable, Tuple

import numpy as np
import pandas as pd

from common.data.yf_loader import load_daily


@dataclass(frozen=True)
class MACDParams:
    fast: int
    slow: int
    signal: int


DATA_DIR = Path(os.getenv("SIGNALS_DATA_DIR", "execution/data"))
CACHE_DIR_RAW = os.getenv("CPO_OUT_DIR", "execution/cache")
if os.path.isabs(CACHE_DIR_RAW):
    CACHE_DIR = Path(CACHE_DIR_RAW)
else:
    base = Path.cwd()
    candidate = (base / CACHE_DIR_RAW).resolve()
    if base == Path("/app") and not candidate.parent.exists():
        CACHE_DIR = base / "cache"
    else:
        CACHE_DIR = candidate
SYMBOL = os.getenv("CPO_SYMBOL", "HDFCBANK.NS")
DEFAULT_LOOKBACK = os.getenv("SIGNAL_LOOKBACK", "2022-01-01")
RISK_PER_TRADE = float(os.getenv("RISK_PER_TRADE", "0.01"))

FILTERS_RAW = os.getenv("MACD_FILTERS", "").strip()
FILTERS: Tuple[str, ...] = tuple(
    f.strip().lower() for f in FILTERS_RAW.split(",") if f.strip()
)

HIST_SIGMA_THRESHOLD = float(os.getenv("MACD_HIST_SIGMA", "0.5"))
TREND_MA_WINDOW = int(os.getenv("MACD_TREND_MA", "200"))
VOLUME_LOOKBACK = int(os.getenv("MACD_VOLUME_LOOKBACK", "20"))
VOLUME_MULTIPLIER = float(os.getenv("MACD_VOLUME_MULTIPLIER", "1.0"))
ATR_LOOKBACK = int(os.getenv("MACD_ATR_LOOKBACK", "14"))
ATR_RATIO_MIN = float(os.getenv("MACD_ATR_RATIO_MIN", "0.0"))
ATR_RATIO_MAX = float(os.getenv("MACD_ATR_RATIO_MAX", "2.0"))


def _latest_params(cache_dir: Path) -> Dict[str, int]:
    files = sorted(cache_dir.glob("macd_params_*.json"))
    if not files:
        raise FileNotFoundError(f"No parameter files found under {cache_dir}")
    with open(files[-1]) as fh:
        return json.load(fh)


def _compute_macd(df: pd.DataFrame, params: MACDParams) -> pd.DataFrame:
    close = df["close"].astype(float)
    macd_fast = close.ewm(span=params.fast, adjust=False).mean()
    macd_slow = close.ewm(span=params.slow, adjust=False).mean()
    macd = macd_fast - macd_slow
    signal = macd.ewm(span=params.signal, adjust=False).mean()
    hist = macd - signal
    return pd.DataFrame(
        {
            "macd": macd,
            "signal": signal,
            "histogram": hist,
            "close": close,
        },
        index=df.index,
    )


def _compute_position(macd_df: pd.DataFrame) -> pd.Series:
    pos = pd.Series(0, index=macd_df.index, dtype=int)
    pos.loc[macd_df["histogram"] > 0] = 1
    pos.loc[macd_df["histogram"] < 0] = -1
    return pos


def _filter_histogram(macd_df: pd.DataFrame) -> bool:
    if not FILTERS:
        return True
    if "histogram" not in FILTERS:
        return True
    hist = macd_df["histogram"].values
    if len(hist) < 2:
        return False
    sigma = np.nanstd(hist[-60:])
    if sigma == 0:
        return False
    return abs(hist[-1]) >= HIST_SIGMA_THRESHOLD * sigma


def _filter_trend(macd_df: pd.DataFrame) -> bool:
    if "trend" not in FILTERS:
        return True
    closes = macd_df["close"]
    if len(closes) < TREND_MA_WINDOW:
        return False
    ma = closes.rolling(TREND_MA_WINDOW).mean().iloc[-1]
    if pd.isna(ma):
        return False
    latest_close = closes.iloc[-1]
    hist_value = macd_df["histogram"].iloc[-1]
    if hist_value > 0:
        return latest_close > ma
    if hist_value < 0:
        return latest_close < ma
    return False


def _filter_volume(df: pd.DataFrame) -> bool:
    if "volume" not in FILTERS:
        return True
    if "volume" not in df:
        return False
    vol = df["volume"].astype(float)
    if len(vol) < VOLUME_LOOKBACK:
        return False
    avg_vol = vol.rolling(VOLUME_LOOKBACK).mean().iloc[-1]
    if pd.isna(avg_vol) or avg_vol == 0:
        return False
    return vol.iloc[-1] >= VOLUME_MULTIPLIER * avg_vol


def _filter_atr(df: pd.DataFrame) -> bool:
    if "atr" not in FILTERS:
        return True
    if not {"high", "low", "close"}.issubset(df.columns):
        return False
    highs = df["high"].astype(float)
    lows = df["low"].astype(float)
    closes = df["close"].astype(float)
    if len(highs) < ATR_LOOKBACK + 1:
        return False
    tr = np.maximum.reduce(
        [
            highs.values[1:] - lows.values[1:],
            np.abs(highs.values[1:] - closes.values[:-1]),
            np.abs(lows.values[1:] - closes.values[:-1]),
        ]
    )
    atr = pd.Series(tr).rolling(ATR_LOOKBACK).mean().iloc[-1]
    if pd.isna(atr) or atr == 0:
        return False
    avg_atr = pd.Series(tr).rolling(ATR_LOOKBACK * 2).mean().iloc[-1]
    if pd.isna(avg_atr) or avg_atr == 0:
        return False
    ratio = atr / avg_atr
    return ATR_RATIO_MIN <= ratio <= ATR_RATIO_MAX


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    params_dict = _latest_params(CACHE_DIR)
    params = MACDParams(**{k: int(v) for k, v in params_dict.items()})

    # Pull data up to today to avoid partial future knowledge
    today = date.today().isoformat()
    start = os.getenv("SIGNAL_DATA_START", DEFAULT_LOOKBACK)
    df = load_daily(SYMBOL, start, today)
    if df.empty:
        raise RuntimeError(f"No price data returned for {SYMBOL}")

    macd_df = _compute_macd(df, params)
    pos = _compute_position(macd_df)
    if len(pos) < 2:
        raise RuntimeError("Not enough history to determine signals")

    prev_pos = int(pos.iloc[-2])
    curr_pos = int(pos.iloc[-1])

    entry = int(curr_pos != 0 and prev_pos == 0)
    exit = int(curr_pos == 0 and prev_pos != 0)
    flip = int(curr_pos != 0 and prev_pos != 0 and curr_pos != prev_pos)

    ts = df.index[-1]
    filters_pass = {
        "histogram": _filter_histogram(macd_df),
        "trend": _filter_trend(macd_df),
        "volume": _filter_volume(df),
        "atr": _filter_atr(df),
    }

    allowed = all(filters_pass[name] for name in FILTERS if name in filters_pass)
    if not allowed:
        entry = 0
        flip = 0
        if curr_pos != 0:
            curr_pos = prev_pos

    out_path = DATA_DIR / f"signals_{ts.date().isoformat()}.csv"
    payload = pd.DataFrame(
        [
            {
                "ts": ts,
                "symbol": SYMBOL,
                "position": curr_pos,
                "entry": entry,
                "exit": exit,
                "flip": flip,
                "close_price": float(df["close"].iloc[-1]),
                "risk_fraction": RISK_PER_TRADE,
                "macd_fast": params.fast,
                "macd_slow": params.slow,
                "macd_signal": params.signal,
            }
        ]
    )
    for name, flag in filters_pass.items():
        payload[f"filter_{name}"] = int(flag)
    payload["filters_applied"] = ",".join(FILTERS)
    payload.to_csv(out_path, index=False)
    print(f"Saved signal row → {out_path}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pragma: no cover - CLI surface
        print(f"Signal build failed: {exc}", file=sys.stderr)
        raise
