"""Walk-forward Bayesian optimisation of MACD parameters for daily strategies."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

from common.data.yf_loader import load_daily
try:
    from execution.param_selector.macd_bayesian import (
        BayesianMacdOptimizer,
        MacdBounds,
        MacdSharpeObjective,
    )
except ImportError:  # when executed from within /app
    from param_selector.macd_bayesian import (  # type: ignore
        BayesianMacdOptimizer,
        MacdBounds,
        MacdSharpeObjective,
    )


@dataclass(frozen=True)
class WFWindowResult:
    train_start: str
    train_end: str
    test_start: str
    test_end: str
    best_fast: int
    best_slow: int
    best_signal: int
    train_sharpe: float
    test_sharpe: float
    trials: List[Dict[str, float]]


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    return int(raw)


def _env_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None:
        return default
    return float(raw)


def _prepare_windows(df: pd.DataFrame, train_days: int, test_days: int) -> List[Tuple[int, int, int, int]]:
    windows: List[Tuple[int, int, int, int]] = []
    total = len(df)
    step = test_days
    max_start = total - (train_days + test_days)
    if max_start <= 0:
        return windows
    for start in range(0, max_start + 1, step):
        train_start = start
        train_end = start + train_days
        test_end = train_end + test_days
        windows.append((train_start, train_end, train_end, min(test_end, total)))
    return windows


def _evaluate_params(close: pd.Series, params: Tuple[int, int, int], cost_bps: float, long_only: bool) -> float:
    objective = MacdSharpeObjective(close, cost_bps=cost_bps, long_only=long_only)
    return objective.evaluate(params)


def main() -> None:
    symbol = os.getenv("CPO_SYMBOL", "HDFCBANK.NS")
    out_dir_raw = os.getenv("CPO_OUT_DIR", "execution/cache")
    out_dir = Path(out_dir_raw)
    out_dir.mkdir(parents=True, exist_ok=True)

    lookback_days = _env_int("MACD_WF_LOOKBACK_DAYS", 5 * 252)
    train_days = _env_int("MACD_WF_TRAIN_DAYS", 3 * 252)
    test_days = _env_int("MACD_WF_TEST_DAYS", 126)
    max_evals = _env_int("MACD_BAYES_MAX_EVALS", 60)
    n_initial = _env_int("MACD_BAYES_N_INIT", 12)
    candidate_pool = _env_int("MACD_BAYES_CANDIDATE_POOL", 300)
    random_state = _env_int("MACD_BAYES_RANDOM_STATE", 42)
    cost_bps = _env_float("MACD_COST_BPS", 5.0)
    long_only = os.getenv("MACD_LONG_ONLY", "true").lower() != "false"

    bounds = MacdBounds(
        fast=(5, int(os.getenv("MACD_FAST_MAX", "40"))),
        slow=(50, int(os.getenv("MACD_SLOW_MAX", "200"))),
        signal=(5, int(os.getenv("MACD_SIGNAL_MAX", "15"))),
        min_slow_gap=_env_int("MACD_MIN_SLOW_GAP", 10),
    )

    today = date.today()
    start_date = (today - timedelta(days=lookback_days * 2)).isoformat()
    df = load_daily(symbol, start_date, today.isoformat()).dropna()
    if df.empty:
        raise RuntimeError(f"No price data returned for {symbol}")
    df = df.tail(lookback_days)

    close_series = df["close"].astype(float)
    windows_idx = _prepare_windows(close_series.to_frame(), train_days, test_days)
    if not windows_idx:
        raise RuntimeError("Not enough data to create walk-forward windows")

    window_results: List[WFWindowResult] = []
    params_list: List[Tuple[int, int, int]] = []

    for train_start, train_end, test_start, test_end in windows_idx:
        train_close = close_series.iloc[train_start:train_end]
        test_close = close_series.iloc[test_start:test_end]

        train_objective = MacdSharpeObjective(train_close, cost_bps=cost_bps, long_only=long_only)
        optimizer = BayesianMacdOptimizer(
            train_objective,
            bounds,
            max_evals=max_evals,
            n_initial=n_initial,
            candidate_pool=candidate_pool,
            random_state=random_state,
        )
        best_params, train_sharpe, history = optimizer.optimize()
        test_sharpe = _evaluate_params(test_close, best_params, cost_bps=cost_bps, long_only=long_only)

        params_list.append(best_params)
        window_results.append(
            WFWindowResult(
                train_start=str(train_close.index[0].date()),
                train_end=str(train_close.index[-1].date()),
                test_start=str(test_close.index[0].date()),
                test_end=str(test_close.index[-1].date()),
                best_fast=best_params[0],
                best_slow=best_params[1],
                best_signal=best_params[2],
                train_sharpe=train_sharpe,
                test_sharpe=test_sharpe,
                trials=history,
            )
        )

    fast_values = [p[0] for p in params_list]
    slow_values = [p[1] for p in params_list]
    signal_values = [p[2] for p in params_list]
    final_fast = int(np.median(fast_values))
    final_slow = int(np.median(slow_values))
    final_signal = int(np.median(signal_values))
    final_params = (final_fast, final_slow, final_signal)

    final_sharpe = _evaluate_params(close_series, final_params, cost_bps=cost_bps, long_only=long_only)

    summary = {
        "fast": final_fast,
        "slow": final_slow,
        "signal": final_signal,
        "cost_bps": cost_bps,
        "long_only": long_only,
        "lookback_days": lookback_days,
        "train_days": train_days,
        "test_days": test_days,
        "max_evals": max_evals,
        "final_sharpe": final_sharpe,
        "windows": len(window_results),
    }

    output_params = out_dir / f"macd_params_{today.isoformat()}.json"
    with output_params.open("w") as fh:
        json.dump(summary, fh)

    history_payload = {
        "symbol": symbol,
        "generated": today.isoformat(),
        "cost_bps": cost_bps,
        "long_only": long_only,
        "window_results": [
            {
                "train_start": r.train_start,
                "train_end": r.train_end,
                "test_start": r.test_start,
                "test_end": r.test_end,
                "fast": r.best_fast,
                "slow": r.best_slow,
                "signal": r.best_signal,
                "train_sharpe": r.train_sharpe,
                "test_sharpe": r.test_sharpe,
                "trials": r.trials,
            }
            for r in window_results
        ],
    }
    output_history = out_dir / f"macd_params_history_{today.isoformat()}.json"
    with output_history.open("w") as fh:
        json.dump(history_payload, fh, indent=2)

    print("Saved params:", output_params)
    print("History log:", output_history)
    print("Final Sharpe:", round(final_sharpe, 4))


if __name__ == "__main__":
    main()
