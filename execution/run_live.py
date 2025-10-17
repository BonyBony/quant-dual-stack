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


RAW_DATA_DIR = os.getenv("SIGNALS_DATA_DIR", "execution/data")
DATA_DIR = Path(RAW_DATA_DIR)
if not DATA_DIR.is_absolute():
    DATA_DIR = (Path.cwd() / DATA_DIR).resolve()

RAW_PNL_FILE = os.getenv("PNL_FILE")
if RAW_PNL_FILE:
    PNL_FILE = Path(RAW_PNL_FILE)
    if not PNL_FILE.is_absolute():
        PNL_FILE = (Path.cwd() / PNL_FILE).resolve()
else:
    PNL_FILE = DATA_DIR / "pnl.csv"
POLL_SECONDS = int(os.getenv("LIVE_POLL_SECONDS", "60"))
MAX_CYCLES_RAW = os.getenv("LIVE_MAX_CYCLES")
if MAX_CYCLES_RAW is None:
    raise RuntimeError("LIVE_MAX_CYCLES must be set (0 for infinite run)")
MAX_CYCLES = int(MAX_CYCLES_RAW)
STOP_AFTER_DATE_RAW = os.getenv("LIVE_STOP_AFTER_DATE")
if not STOP_AFTER_DATE_RAW:
    raise RuntimeError("LIVE_STOP_AFTER_DATE must be set (ISO format YYYY-MM-DD)")
try:
    STOP_AFTER_DATE = datetime.fromisoformat(STOP_AFTER_DATE_RAW).date()
except ValueError as exc:
    raise RuntimeError(
        "LIVE_STOP_AFTER_DATE must be in ISO format YYYY-MM-DD"
    ) from exc
DEFAULT_ORDER_TYPE = os.getenv("UPSTOX_ORDER_TYPE", "LIMIT").upper()
EXIT_ORDER_TYPE = os.getenv("UPSTOX_EXIT_ORDER_TYPE", DEFAULT_ORDER_TYPE).upper()
PRICE_BUFFER_BPS = float(os.getenv("ORDER_PRICE_BUFFER_BPS", "0"))
DEFAULT_QUANTITY = float(os.getenv("ORDER_DEFAULT_QUANTITY", "1"))
COST_BPS = float(os.getenv("MACD_COST_BPS", "5.0"))
LONG_ONLY = os.getenv("MACD_LONG_ONLY", "true").lower() != "false"

RAW_ORDER_LOG = os.getenv("ORDER_LOG_FILE", "data/orders.csv")
ORDER_LOG_FILE = Path(RAW_ORDER_LOG)
if not ORDER_LOG_FILE.is_absolute():
    ORDER_LOG_FILE = (Path.cwd() / ORDER_LOG_FILE).resolve()


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


def _append_order(**row: float | str | int | None) -> None:
    ORDER_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame([row])
    df.to_csv(ORDER_LOG_FILE, mode="a", header=not ORDER_LOG_FILE.exists(), index=False)


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    client = UpstoxClient()
    last_ts = None
    last_position = 0
    last_price = 0.0
    last_size = DEFAULT_QUANTITY
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
        target_size = float(sig_row.get("target_position_size", DEFAULT_QUANTITY))
        expected_cost = float(sig_row.get("expected_cost_pct", COST_BPS / 10_000.0))
        long_only_flag = bool(int(sig_row.get("long_only", int(LONG_ONLY)))) if "long_only" in sig_row else LONG_ONLY

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
            qty = target_size if pos > 0 else target_size
            req = _build_order(side, qty, DEFAULT_ORDER_TYPE)
            order_id = client.place_order(req)
            _append_order(
                ts=datetime.utcnow(),
                signal_ts=ts,
                symbol=symbol,
                side=side,
                order_type=req.order_type,
                action="ENTRY" if entry and not flip else "FLIP",
                quantity=req.quantity,
                price=req.price,
                trigger_price=req.trigger_price,
                order_id=order_id,
            )
            last_position = pos
            last_size = req.quantity
            placed = True
        elif exit_sig and last_position:
            side = "SELL" if last_position > 0 else "BUY"
            base_price = close_price or last_price
            exit_price = None
            exit_trigger = None
            if EXIT_ORDER_TYPE != "MARKET":
                computed = _order_price(base_price, side, PRICE_BUFFER_BPS)
                if computed is None:
                    raise ValueError("Unable to derive exit price for limit order")
                if EXIT_ORDER_TYPE == "SL-M":
                    exit_trigger = computed
                else:
                    exit_price = computed
                    exit_trigger = computed

            order_id = client.close_position(
                symbol,
                quantity=abs(last_size),
                side=side,
                order_type=EXIT_ORDER_TYPE,
                price=round(exit_price, 2) if exit_price is not None else None,
                trigger_price=round(exit_trigger, 2) if exit_trigger is not None else None,
            )
            logging.info("Submitted close order %s", order_id)
            _append_order(
                ts=datetime.utcnow(),
                signal_ts=ts,
                symbol=symbol,
                side=side,
                order_type=EXIT_ORDER_TYPE,
                action="EXIT",
                quantity=abs(last_size),
                price=round(exit_price, 2) if exit_price is not None else None,
                trigger_price=round(exit_trigger, 2) if exit_trigger is not None else None,
                order_id=order_id,
            )
            last_position = 0
            last_size = DEFAULT_QUANTITY
            placed = True
        else:
            logging.info("No actionable change (holding position %s)", pos)
            last_position = pos

        last_price = close_price or last_price
        last_ts = ts
        mark_value = last_position * (close_price or last_price)
        _append_pnl(eq_value=mark_value)

        cycles += 1
        if MAX_CYCLES == 0:
            pass
        else:
            if STOP_AFTER_DATE and ts.date() >= STOP_AFTER_DATE:
                logging.info(
                    "Reached stop date %s (last signal %s); exiting live loop",
                    STOP_AFTER_DATE,
                    ts.date(),
                )
                break
            if MAX_CYCLES and cycles >= MAX_CYCLES:
                logging.info("Reached max cycles (%s); exiting live loop", MAX_CYCLES)
                break

        if placed:
            time.sleep(max(POLL_SECONDS, 1))
        else:
            time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
