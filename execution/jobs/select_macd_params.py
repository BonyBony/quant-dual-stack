"""Select MACD parameters via Bayesian optimisation on Sharpe ratio."""

from __future__ import annotations

import json
import os
from datetime import date, timedelta
from pathlib import Path

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


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError as exc:
        raise ValueError(f"Environment variable {name} must be an integer") from exc


def main() -> None:
    symbol = os.getenv("CPO_SYMBOL", "HDFCBANK.NS")
    out_dir = Path(os.getenv("CPO_OUT_DIR", "execution/cache"))
    out_dir.mkdir(parents=True, exist_ok=True)

    lookback_days = _env_int("MACD_BAYES_LOOKBACK_DAYS", 365)
    max_evals = _env_int("MACD_BAYES_MAX_EVALS", 40)
    n_initial = _env_int("MACD_BAYES_N_INIT", 8)
    min_gap = _env_int("MACD_BAYES_MIN_SLOW_GAP", 5)
    candidate_pool = _env_int("MACD_BAYES_CANDIDATE_POOL", 200)

    today = date.today()
    start = os.getenv("SIGNAL_DATA_START")
    if not start:
        start = (today - timedelta(days=lookback_days * 2)).isoformat()

    df = load_daily(symbol, start, today.isoformat()).dropna()
    if df.empty:
        raise RuntimeError(f"No price data returned for {symbol}")

    df = df.tail(lookback_days * 2)
    close = df["close"].astype(float)

    objective = MacdSharpeObjective(close)
    bounds = MacdBounds(fast=(5, 20), slow=(25, 80), signal=(3, 15), min_slow_gap=min_gap)

    optimizer = BayesianMacdOptimizer(
        objective,
        bounds,
        max_evals=max_evals,
        n_initial=n_initial,
        candidate_pool=candidate_pool,
        random_state=_env_int("MACD_BAYES_RANDOM_STATE", 42),
    )

    best_params, best_score, history = optimizer.optimize()

    payload = {"fast": int(best_params[0]), "slow": int(best_params[1]), "signal": int(best_params[2])}
    target_path = out_dir / f"macd_params_{today.isoformat()}.json"
    with target_path.open("w") as fh:
        json.dump(payload, fh)

    history_path = out_dir / f"macd_params_history_{today.isoformat()}.json"
    with history_path.open("w") as fh:
        json.dump({"best_sharpe": best_score, "trials": history}, fh, indent=2)

    print("Saved params:", target_path)
    print("Best Sharpe:", round(best_score, 4))
    print("History log:", history_path)


if __name__ == "__main__":
    main()
