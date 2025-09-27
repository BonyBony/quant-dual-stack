"""Polling loop that consumes signal CSVs and routes orders (dry run)."""

from __future__ import annotations

import logging
import os
import time
from datetime import datetime
from pathlib import Path

import pandas as pd

from execution.brokers.upstox_client import OrderRequest, UpstoxClient


DATA_DIR = Path("execution/data")
PNL_FILE = DATA_DIR / "pnl.csv"
POLL_SECONDS = int(os.getenv("LIVE_POLL_SECONDS", "60"))


def _latest_signal() -> tuple[pd.Series, Path] | tuple[None, None]:
    files = sorted(DATA_DIR.glob("signals_*.csv"))
    if not files:
        return None, None
    df = pd.read_csv(files[-1], parse_dates=["ts"])
    if df.empty:
        return None, files[-1]
    df = df.sort_values("ts")
    return df.iloc[-1], files[-1]


def _append_pnl(eq_value: float) -> None:
    PNL_FILE.parent.mkdir(parents=True, exist_ok=True)
    row = pd.DataFrame({"ts": [datetime.utcnow()], "eq": [eq_value]})
    row.to_csv(PNL_FILE, mode="a", header=not PNL_FILE.exists(), index=False)


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    client = UpstoxClient()
    last_ts = None

    while True:
        sig_row, sig_path = _latest_signal()
        if sig_row is None:
            time.sleep(POLL_SECONDS)
            continue

        ts = pd.Timestamp(sig_row["ts"]) if not isinstance(sig_row["ts"], pd.Timestamp) else sig_row["ts"]
        if last_ts == ts:
            time.sleep(POLL_SECONDS)
            continue

        symbol = str(sig_row.get("symbol", ""))
        pos = int(sig_row.get("position", 0))
        entry = bool(sig_row.get("entry", 0))
        exit_sig = bool(sig_row.get("exit", 0))
        flip = bool(sig_row.get("flip", 0))
        risk_fraction = float(sig_row.get("risk_fraction", 0.0))

        logging.info("Processing signal %s from %s", ts, sig_path.name)

        if flip or entry:
            side = "BUY" if pos > 0 else "SELL"
            qty = max(1.0, abs(pos) * max(risk_fraction, 1.0))
            req = OrderRequest(symbol=symbol, side=side, quantity=qty)
            client.place_order(req)
        elif exit_sig:
            client.close_position(symbol)
        else:
            logging.info("No actionable change (holding position %s)", pos)

        last_ts = ts
        _append_pnl(eq_value=0.0)  # placeholder until broker fill updates arrive
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
