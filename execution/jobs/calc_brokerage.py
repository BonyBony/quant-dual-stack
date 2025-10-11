"""Compute brokerage cost comparison between Upstox (per-order) and Zerodha (flat monthly)."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

UPSTOX_COST_PER_ORDER = 10.0  # INR
ZERODHA_MONTHLY_COST = 500.0  # INR


def load_orders(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"Order log not found: {csv_path}")
    df = pd.read_csv(csv_path)
    if df.empty:
        raise ValueError("Order log is empty")
    if "ts" not in df.columns:
        raise ValueError("Order log must contain a 'ts' column")
    df["ts"] = pd.to_datetime(df["ts"], utc=False)
    df["month"] = df["ts"].dt.to_period("M")
    return df


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby("month").agg(
        orders=("order_id", "count"),
        symbols=("symbol", lambda s: sorted(set(s))),
    )
    grouped["symbols"] = grouped["symbols"].apply(lambda lst: ",".join(lst))
    grouped = grouped.reset_index()
    grouped["month_start"] = grouped["month"].dt.to_timestamp()
    grouped["upstox_cost"] = grouped["orders"] * UPSTOX_COST_PER_ORDER
    grouped["zerodha_cost"] = grouped["orders"].apply(
        lambda n: ZERODHA_MONTHLY_COST if n > 0 else 0.0
    )
    grouped["cost_diff"] = grouped["upstox_cost"] - grouped["zerodha_cost"]
    grouped["break_even_orders"] = ZERODHA_MONTHLY_COST / UPSTOX_COST_PER_ORDER
    return grouped[
        [
            "month_start",
            "orders",
            "symbols",
            "upstox_cost",
            "zerodha_cost",
            "cost_diff",
            "break_even_orders",
        ]
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--order-log",
        default="data/orders.csv",
        type=Path,
        help="Path to the CSV created by run_live.py",
    )
    args = parser.parse_args()

    df = load_orders(args.order_log)
    summary = summarize(df)

    print("Monthly brokerage comparison (INR):")
    print(summary.to_string(index=False))

    total_orders = int(df.shape[0])
    total_upstox = total_orders * UPSTOX_COST_PER_ORDER
    # Zerodha cost: number of unique months with orders times monthly cost.
    months_with_orders = summary[summary["orders"] > 0].shape[0]
    total_zerodha = months_with_orders * ZERODHA_MONTHLY_COST

    print("\nTotals:")
    print(f"  Total orders: {total_orders}")
    print(f"  Upstox cost: INR {total_upstox:.2f}")
    print(f"  Zerodha cost: INR {total_zerodha:.2f}")
    if total_orders > 0:
        print(
            f"  Average cost/order (Upstox): INR {UPSTOX_COST_PER_ORDER:.2f};"
            f" break-even at {ZERODHA_MONTHLY_COST / UPSTOX_COST_PER_ORDER:.0f} orders/month"
        )


if __name__ == "__main__":
    main()
