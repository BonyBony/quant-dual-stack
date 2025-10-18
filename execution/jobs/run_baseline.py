"""Run the MACD WF long-only baseline and save benchmark artefacts."""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml

from common.data.yf_loader import load_daily

plt.switch_backend("Agg")


def zscore(series: pd.Series) -> pd.Series:
    return (series - series.mean()) / (series.std(ddof=0) + 1e-9)


def macd_components(close: pd.Series, fast: int, slow: int, signal: int) -> pd.DataFrame:
    fast_ema = close.ewm(span=fast, adjust=False).mean()
    slow_ema = close.ewm(span=slow, adjust=False).mean()
    macd = fast_ema - slow_ema
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    hist = macd - signal_line
    return pd.DataFrame({"macd": macd, "signal": signal_line, "hist": hist})


def compute_rsi(close: pd.Series, length: int) -> pd.Series:
    delta = close.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    gain = up.ewm(alpha=1 / length, adjust=False, min_periods=length).mean()
    loss = down.ewm(alpha=1 / length, adjust=False, min_periods=length).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def compute_mfi(df: pd.DataFrame, length: int) -> pd.Series:
    if not {"high", "low", "close", "volume"}.issubset(df.columns):
        return pd.Series(dtype=float, index=df.index)
    tp = (df["high"] + df["low"] + df["close"]) / 3
    mf = tp * df["volume"]
    pos = np.where(tp > tp.shift(1), mf, 0.0)
    neg = np.where(tp < tp.shift(1), mf, 0.0)
    pos_flow = pd.Series(pos, index=df.index).rolling(length).sum()
    neg_flow = pd.Series(neg, index=df.index).rolling(length).sum().replace(0, np.nan)
    ratio = pos_flow / neg_flow
    return 100 - (100 / (1 + ratio))


def atr_series(df: pd.DataFrame, length: int) -> pd.Series:
    if not {"high", "low", "close"}.issubset(df.columns):
        return pd.Series(dtype=float, index=df.index)
    high, low, close = df["high"], df["low"], df["close"]
    prev_close = close.shift(1)
    tr = pd.concat([
        (high - low),
        (high - prev_close).abs(),
        (low - prev_close).abs(),
    ], axis=1).max(axis=1)
    return tr.rolling(length).mean()


def build_position(
    df: pd.DataFrame,
    config: Dict,
) -> pd.Series:
    hist = df["hist"].dropna()
    # long-only desired signal
    desired = pd.Series(np.where(hist > 0, 1, 0), index=hist.index)
    desired.replace(0, method="ffill", inplace=True)
    desired = desired.reindex(df.index).fillna(0).astype(int)

    allow = pd.Series(True, index=df.index)

    hist_sigma = config["filters"].get("histogram", {}).get("sigma", 0.0)
    if hist_sigma > 0:
        sigma = df["hist"].rolling(60).std()
        allow &= (df["hist"].abs() >= hist_sigma * sigma).fillna(False)

    if config["filters"].get("weekly_trend", True):
        weekly = df["hist"].resample("W-FRI").last().reindex(df.index, method="ffill")
        allow &= (weekly > 0).fillna(False)

    confirm_bars = config["filters"].get("confirm_bars", 0)
    if confirm_bars > 0:
        allow &= (df["hist"].rolling(confirm_bars).apply(lambda s: (s > 0).all(), raw=False) > 0).fillna(False)

    rsi_cfg = config["filters"].get("rsi", {})
    if rsi_cfg:
        rsi = compute_rsi(df["close"], rsi_cfg.get("length", 14))
        allow &= (rsi <= rsi_cfg.get("max", 60)).fillna(False)

    mfi_cfg = config["filters"].get("mfi", {})
    if mfi_cfg:
        mfi = compute_mfi(df, mfi_cfg.get("length", 14))
        bars = mfi_cfg.get("rise_bars", 1)
        allow &= (mfi > mfi.shift(bars)).fillna(False)

    volume_cfg = config["filters"].get("volume", {})
    if volume_cfg and "volume" in df:
        avg_vol = df["volume"].rolling(volume_cfg.get("lookback", 20)).mean()
        allow &= (df["volume"] >= volume_cfg.get("multiplier", 1.0) * avg_vol).fillna(False)

    atr_cfg = config["filters"].get("atr", {})
    if atr_cfg:
        atr = atr_series(df, atr_cfg.get("lookback", 14))
        avg_atr = atr.rolling(atr_cfg.get("lookback", 14) * 2).mean()
        ratio = atr / avg_atr
        allow &= ((ratio >= atr_cfg.get("min_ratio", 0.0)) & (ratio <= atr_cfg.get("max_ratio", 2.0))).fillna(False)

    position = pd.Series(0, index=df.index, dtype=int)
    for i in range(1, len(df)):
        if desired.iloc[i] != position.iloc[i - 1]:
            position.iloc[i] = desired.iloc[i] if allow.iloc[i] else position.iloc[i - 1]
        else:
            position.iloc[i] = position.iloc[i - 1]
    return position


def compute_metrics(position: pd.Series, close: pd.Series, cost_bps: float) -> dict:
    returns = close.pct_change().fillna(0.0)
    pos = position.shift(1).fillna(0)
    strat_returns = pos * returns
    trades = pos.diff().abs()
    strat_returns -= trades * (cost_bps / 10_000)

    curve = (1 + strat_returns).cumprod()
    total_return = curve.iloc[-1] - 1
    trading_days = len(strat_returns)
    cagr = (1 + total_return) ** (252 / trading_days) - 1 if trading_days else 0.0
    vol = strat_returns.std(ddof=0)
    sharpe = (strat_returns.mean() / vol * math.sqrt(252)) if vol > 0 else 0.0
    drawdown = curve / curve.cummax() - 1
    turnover = trades.mean() * 252

    return {
        "returns": strat_returns,
        "curve": curve,
        "total_return": total_return,
        "cagr": cagr,
        "sharpe": sharpe,
        "max_drawdown": drawdown.min(),
        "ann_vol": vol * math.sqrt(252),
        "turnover": turnover,
        "trades": int(trades.sum()),
        "win_rate": float((strat_returns[strat_returns != 0] > 0).mean()),
    }


def build_trade_log(position: pd.Series, close: pd.Series, cost_bps: float) -> pd.DataFrame:
    pos_shift = position.shift(1).fillna(0)
    change = position - pos_shift
    trades = change[change != 0]
    records = []
    for ts, qty in trades.items():
        records.append(
            {
                "date": ts,
                "quantity": qty,
                "price": close.loc[ts],
                "cost_bps": cost_bps,
            }
        )
    return pd.DataFrame(records)


def run_baseline(config_path: Path) -> None:
    with open(config_path, "r") as fh:
        cfg = yaml.safe_load(fh)

    symbol = cfg["symbol"]
    start = cfg["start_date"]
    end = cfg["end_date"] or date.today().isoformat()
    cost_bps = float(cfg.get("cost_bps", 0.0))

    price_df = load_daily(symbol, start, end).dropna()
    macd_cfg = cfg["macd"]
    macd_df = macd_components(price_df["close"], macd_cfg["fast"], macd_cfg["slow"], macd_cfg["signal"])
    df = price_df.join(macd_df, how="inner")

    position = build_position(df, cfg)
    strat_metrics = compute_metrics(position, df["close"], cost_bps)

    bh_returns = df["close"].pct_change().fillna(0.0)
    bh_curve = (1 + bh_returns).cumprod()
    bh_metrics = {
        "total_return": bh_curve.iloc[-1] - 1,
        "cagr": (bh_curve.iloc[-1]) ** (252 / len(bh_returns)) - 1,
        "sharpe": (bh_returns.mean() / bh_returns.std(ddof=0) * math.sqrt(252)),
        "max_drawdown": (bh_curve / bh_curve.cummax() - 1).min(),
        "ann_vol": bh_returns.std(ddof=0) * math.sqrt(252),
    }

    results_row = {
        "strategy": "MACD_WF_long_only",
        "symbol": symbol,
        "start": df.index[0].date().isoformat(),
        "end": df.index[-1].date().isoformat(),
        "sharpe_net": strat_metrics["sharpe"],
        "cagr": strat_metrics["cagr"],
        "total_return": strat_metrics["total_return"],
        "max_drawdown": strat_metrics["max_drawdown"],
        "ann_vol": strat_metrics["ann_vol"],
        "turnover": strat_metrics["turnover"],
        "trades": strat_metrics["trades"],
        "win_rate": strat_metrics["win_rate"],
        "bh_sharpe": bh_metrics["sharpe"],
        "bh_total_return": bh_metrics["total_return"],
    }

    results_path = Path(cfg["outputs"]["results_csv"])
    results_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([results_row]).to_csv(results_path, index=False)

    fig, ax = plt.subplots(figsize=(10, 5))
    strat_metrics["curve"].plot(ax=ax, label="MACD WF long-only")
    bh_curve.plot(ax=ax, label="Buy & Hold")
    ax.set_title(f"Baseline vs Buy & Hold ({symbol})")
    ax.set_ylabel("Cumulative return")
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()
    Path(cfg["outputs"]["equity_curve_png"]).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(cfg["outputs"]["equity_curve_png"], dpi=150)
    plt.close(fig)

    trade_log = build_trade_log(position, df["close"], cost_bps)
    trade_path = Path(cfg["outputs"]["trade_log_parquet"])
    trade_path.parent.mkdir(parents=True, exist_ok=True)
    trade_log.to_parquet(trade_path, index=False)

    print(json.dumps(results_row, indent=2))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run MACD baseline experiment")
    parser.add_argument("--config", required=True, help="Path to baseline config.yaml")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_baseline(Path(args.config))
