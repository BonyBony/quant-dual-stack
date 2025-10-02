"""Polling loop that consumes signal CSVs and routes orders (dry run)."""

from __future__ import annotations

import logging
import os
import time
from datetime import datetime
from pathlib import Path

import pandas as pd

try:
    from execution.brokers.upstox_client import OrderRequest, UpstoxClient
except ImportError:  # when run as script from package root
    from brokers.upstox_client import OrderRequest, UpstoxClient  # type: ignore


DATA_DIR = Path("execution/data")
PNL_FILE = DATA_DIR / "pnl.csv"
POLL_SECONDS = int(os.getenv("LIVE_POLL_SECONDS", "60"))
MAX_CYCLES = int(os.getenv("LIVE_MAX_CYCLES", "0"))
DEFAULT_ORDER_TYPE = os.getenv("UPSTOX_ORDER_TYPE", "LIMIT").upper()
EXIT_ORDER_TYPE = os.getenv("UPSTOX_EXIT_ORDER_TYPE", DEFAULT_ORDER_TYPE).upper()
PRICE_BUFFER_BPS = float(os.getenv("ORDER_PRICE_BUFFER_BPS", "0"))
DEFAULT_QUANTITY = float(os.getenv("ORDER_DEFAULT_QUANTITY", "1"))


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
    last_position = 0
    last_price = 0.0
    cycles = 0

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
        close_price = float(sig_row.get("close_price", 0.0))

        logging.info("Processing signal %s from %s", ts, sig_path.name)

        def _order_price(base: float, side: str, buffer_bps: float) -> float | None:
            if base <= 0:
                return None
            if buffer_bps == 0:
                return base
            direction = 1 if side == "BUY" else -1
            return base * (1 + direction * buffer_bps / 10_000)

        def _build_order(side: str, quantity: float, order_type: str) -> OrderRequest:
            base_price = close_price or last_price
            price = _order_price(base_price, side, PRICE_BUFFER_BPS) if order_type != "MARKET" else None
            trigger = price if order_type != "MARKET" else None
            kwargs = {
                "symbol": symbol,
                "side": side,
                "quantity": max(quantity, DEFAULT_QUANTITY),
                "order_type": order_type,
            }
            if price is not None:
                kwargs["price"] = round(price, 2)
            if trigger is not None:
                kwargs["trigger_price"] = round(trigger, 2)
            return OrderRequest(**kwargs)

        placed = False
        if flip or entry:
            side = "BUY" if pos > 0 else "SELL"
            qty = abs(pos) if pos != 0 else DEFAULT_QUANTITY
            req = _build_order(side, qty, DEFAULT_ORDER_TYPE)
            client.place_order(req)
            last_position = pos
            placed = True
        elif exit_sig and last_position:
            side = "SELL" if last_position > 0 else "BUY"
            qty = abs(last_position)
            req = _build_order(side, qty, EXIT_ORDER_TYPE)
            client.place_order(req)
            last_position = 0
            placed = True
        else:
            logging.info("No actionable change (holding position %s)", pos)
            last_position = pos

        last_price = close_price or last_price
        last_ts = ts
        mark_value = last_position * (close_price or last_price)
        _append_pnl(eq_value=mark_value)

        cycles += 1
        if MAX_CYCLES and cycles >= MAX_CYCLES:
            logging.info("Reached max cycles (%s); exiting live loop", MAX_CYCLES)
            break

        if placed:
            time.sleep(max(POLL_SECONDS, 1))
        else:
            time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
