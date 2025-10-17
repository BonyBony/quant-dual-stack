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
LONG_ONLY = os.getenv("MACD_LONG_ONLY", "true").lower() != "false"
CONFIRM_BARS = int(os.getenv("MACD_CONFIRM_BARS", "3"))
RSI_LENGTH = int(os.getenv("MACD_RSI_LENGTH", "14"))
RSI_MAX = float(os.getenv("MACD_RSI_MAX", "60"))
MFI_LENGTH = int(os.getenv("MACD_MFI_LENGTH", "14"))
MFI_RISE_BARS = int(os.getenv("MACD_MFI_RISE_BARS", "1"))
COST_BPS = float(os.getenv("MACD_COST_BPS", "5.0"))
RISK_BUDGET = float(os.getenv("MACD_RISK_BUDGET", "0.01"))
DEFAULT_QUANTITY = float(os.getenv("ORDER_DEFAULT_QUANTITY", "1.0"))


def _latest_params(cache_dir: Path) -> Dict[str, int]:
    files = sorted(
        f for f in cache_dir.glob("macd_params_*.json") if "history" not in f.name
    )
    if not files:
        raise FileNotFoundError(f"No parameter files found under {cache_dir}")
    with open(files[-1]) as fh:
        data = json.load(fh)
    return {
        "fast": int(data["fast"]),
        "slow": int(data["slow"]),
        "signal": int(data["signal"]),
    }


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
    if LONG_ONLY:
        pos = pd.Series(0, index=macd_df.index, dtype=int)
        pos.loc[macd_df["histogram"] > 0] = 1
    else:
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


def _filter_weekly(macd_df: pd.DataFrame) -> bool:
    if "weekly" not in FILTERS:
        return True
    hist = macd_df["histogram"]
    if not isinstance(hist.index, pd.DatetimeIndex):
        return False
    weekly = hist.resample("W-FRI").last().dropna()
    if weekly.empty:
        return False
    if weekly.iloc[-1] > 0:
        return True
    if not LONG_ONLY:
        return weekly.iloc[-1] < 0
    return False


def _filter_confirmation(macd_df: pd.DataFrame) -> bool:
    if "confirm" not in FILTERS:
        return True
    hist = macd_df["histogram"].dropna()
    if len(hist) < CONFIRM_BARS:
        return False
    window = hist.iloc[-CONFIRM_BARS:]
    if LONG_ONLY:
        return (window > 0).all()
    if window.iloc[-1] > 0:
        return (window > 0).all()
    if window.iloc[-1] < 0:
        return (window < 0).all()
    return False


def _compute_rsi(series: pd.Series, length: int) -> pd.Series:
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    gain = up.ewm(alpha=1 / length, adjust=False, min_periods=length).mean()
    loss = down.ewm(alpha=1 / length, adjust=False, min_periods=length).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def _filter_rsi(df: pd.DataFrame) -> bool:
    if "rsi" not in FILTERS:
        return True
    rsi = _compute_rsi(df["close"].astype(float), RSI_LENGTH)
    if rsi.empty or pd.isna(rsi.iloc[-1]):
        return False
    return rsi.iloc[-1] <= RSI_MAX


def _compute_mfi(df: pd.DataFrame, length: int) -> pd.Series:
    if not {"high", "low", "close", "volume"}.issubset(df.columns):
        return pd.Series(dtype=float)
    high = df["high"].astype(float)
    low = df["low"].astype(float)
    close = df["close"].astype(float)
    volume = df["volume"].astype(float)
    typical_price = (high + low + close) / 3
    money_flow = typical_price * volume
    positive = money_flow.where(typical_price > typical_price.shift(1), 0.0)
    negative = money_flow.where(typical_price < typical_price.shift(1), 0.0)
    positive_flow = positive.rolling(length).sum()
    negative_flow = negative.rolling(length).sum()
    ratio = positive_flow / negative_flow.replace(0.0, np.nan)
    mfi = 100 - (100 / (1 + ratio))
    return mfi


def _filter_mfi(df: pd.DataFrame) -> bool:
    if "mfi" not in FILTERS:
        return True
    mfi = _compute_mfi(df, MFI_LENGTH)
    if mfi.empty or len(mfi.dropna()) < MFI_RISE_BARS + 1:
        return False
    latest = mfi.iloc[-1]
    prev = mfi.iloc[-(MFI_RISE_BARS + 1)]
    if pd.isna(latest) or pd.isna(prev):
        return False
    if LONG_ONLY:
        return latest > prev
    return latest > prev if mfi.iloc[-1] > 50 else True


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


def _compute_atr_series(df: pd.DataFrame, lookback: int) -> pd.Series:
    if not {"high", "low", "close"}.issubset(df.columns):
        return pd.Series(dtype=float)
    high = df["high"].astype(float)
    low = df["low"].astype(float)
    close = df["close"].astype(float)
    prev_close = close.shift(1)
    tr = pd.concat([
        (high - low),
        (high - prev_close).abs(),
        (low - prev_close).abs(),
    ], axis=1).max(axis=1)
    atr = tr.rolling(lookback).mean()
    return atr


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
        "weekly": _filter_weekly(macd_df),
        "confirm": _filter_confirmation(macd_df),
        "rsi": _filter_rsi(df),
        "mfi": _filter_mfi(df),
        "volume": _filter_volume(df),
        "atr": _filter_atr(df),
    }

    allowed = all(filters_pass[name] for name in FILTERS if name in filters_pass)
    if not allowed:
        entry = 0
        flip = 0
        if curr_pos != 0:
            curr_pos = prev_pos

    atr_series = _compute_atr_series(df, ATR_LOOKBACK)
    latest_atr = float(atr_series.dropna().iloc[-1]) if not atr_series.dropna().empty else float("nan")
    latest_price = float(df["close"].iloc[-1])
    if np.isnan(latest_atr) or latest_atr <= 0 or latest_price <= 0:
        target_size = DEFAULT_QUANTITY
    else:
        atr_pct = latest_atr / latest_price
        if atr_pct <= 0:
            target_size = DEFAULT_QUANTITY
        else:
            target_size = max(DEFAULT_QUANTITY, RISK_BUDGET / atr_pct)

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
                "target_position_size": target_size,
                "expected_cost_pct": COST_BPS / 10_000.0,
                "long_only": int(LONG_ONLY),
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
