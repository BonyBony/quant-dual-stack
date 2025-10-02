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
from datetime import date
from pathlib import Path
from typing import Dict

import pandas as pd

from common.data.yf_loader import load_daily

try:
    from research.strategies.macd import MACDParams
except ImportError:  # pragma: no cover - execution path without research mounted
    from dataclasses import dataclass

    @dataclass(frozen=True)
    class MACDParams:  # type: ignore[override]
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


def _latest_params(cache_dir: Path) -> Dict[str, int]:
    files = sorted(cache_dir.glob("macd_params_*.json"))
    if not files:
        raise FileNotFoundError(f"No parameter files found under {cache_dir}")
    with open(files[-1]) as fh:
        return json.load(fh)


def _compute_position(df: pd.DataFrame, params: MACDParams) -> pd.Series:
    close = df["close"].astype(float)
    macd = close.ewm(span=params.fast, adjust=False).mean() - close.ewm(
        span=params.slow, adjust=False
    ).mean()
    signal = macd.ewm(span=params.signal, adjust=False).mean()
    hist = macd - signal
    pos = pd.Series(0, index=close.index, dtype=int)
    pos.loc[hist > 0] = 1
    pos.loc[hist < 0] = -1
    return pos


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

    pos = _compute_position(df, params)
    if len(pos) < 2:
        raise RuntimeError("Not enough history to determine signals")

    prev_pos = int(pos.iloc[-2])
    curr_pos = int(pos.iloc[-1])

    entry = int(curr_pos != 0 and prev_pos == 0)
    exit = int(curr_pos == 0 and prev_pos != 0)
    flip = int(curr_pos != 0 and prev_pos != 0 and curr_pos != prev_pos)

    ts = df.index[-1]
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
    payload.to_csv(out_path, index=False)
    print(f"Saved signal row → {out_path}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pragma: no cover - CLI surface
        print(f"Signal build failed: {exc}", file=sys.stderr)
        raise
