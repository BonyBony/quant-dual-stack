"""Bayesian optimisation of MACD parameters using Sharpe ratio as objective."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np
import pandas as pd
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel, Matern, WhiteKernel


@dataclass(frozen=True)
class MacdBounds:
    fast: Tuple[int, int]
    slow: Tuple[int, int]
    signal: Tuple[int, int]
    min_slow_gap: int = 5


class MacdSharpeObjective:
    """Evaluate MACD strategy Sharpe ratio for a set of parameters."""

    def __init__(self, close: pd.Series) -> None:
        clean = close.dropna().astype(float)
        if clean.empty:
            raise ValueError("Close price series is empty")
        self.close = clean

    def evaluate(self, params: Sequence[int]) -> float:
        fast, slow, signal = params
        if fast >= slow or signal <= 0:
            return float("-inf")

        close = self.close
        macd_fast = close.ewm(span=fast, adjust=False).mean()
        macd_slow = close.ewm(span=slow, adjust=False).mean()
        macd = macd_fast - macd_slow
        macd_signal = macd.ewm(span=signal, adjust=False).mean()
        hist = macd - macd_signal

        position = pd.Series(0.0, index=close.index)
        position.loc[hist > 0] = 1.0
        position.loc[hist < 0] = -1.0
        position = position.shift(1).fillna(0.0)  # enter next day

        returns = close.pct_change().fillna(0.0)
        strat_returns = position * returns
        if strat_returns.std(ddof=0) == 0:
            return float("-inf")
        sharpe = strat_returns.mean() / strat_returns.std(ddof=0) * math.sqrt(252)
        if math.isnan(sharpe):
            return float("-inf")
        return float(sharpe)


class BayesianMacdOptimizer:
    def __init__(
        self,
        objective: MacdSharpeObjective,
        bounds: MacdBounds,
        *,
        max_evals: int = 40,
        n_initial: int = 8,
        candidate_pool: int = 200,
        random_state: int | None = None,
    ) -> None:
        if max_evals <= 0:
            raise ValueError("max_evals must be positive")
        if n_initial <= 0:
            raise ValueError("n_initial must be positive")
        self.objective = objective
        self.bounds = bounds
        self.max_evals = max_evals
        self.n_initial = min(n_initial, max_evals)
        self.candidate_pool = max(candidate_pool, 50)
        self.rng = random.Random(random_state)

        self._evaluated: Dict[Tuple[int, int, int], float] = {}
        self._x_train: List[Tuple[int, int, int]] = []
        self._y_train: List[float] = []

        self._scale_vector = np.array(
            [bounds.fast[1], bounds.slow[1], bounds.signal[1]], dtype=float
        )

    # ------------------------------------------------------------------
    def optimize(self) -> Tuple[Tuple[int, int, int], float, List[Dict[str, float]]]:
        history: List[Dict[str, float]] = []
        best_params = None
        best_score = float("-inf")

        for iteration in range(self.max_evals):
            if iteration < self.n_initial or len(self._x_train) < self.n_initial:
                params = self._sample_random()
            else:
                params = self._propose()

            score = self.objective.evaluate(params)
            self._register(params, score)

            if score > best_score:
                best_score = score
                best_params = params

            history.append(
                {
                    "iteration": iteration + 1,
                    "fast": params[0],
                    "slow": params[1],
                    "signal": params[2],
                    "sharpe": score,
                }
            )

        if best_params is None:
            raise RuntimeError("Bayesian optimisation failed to evaluate any parameters")

        return best_params, best_score, history

    # ------------------------------------------------------------------
    def _register(self, params: Tuple[int, int, int], score: float) -> None:
        self._evaluated[params] = score
        self._x_train.append(params)
        self._y_train.append(score)

    def _sample_random(self) -> Tuple[int, int, int]:
        fast_min, fast_max = self.bounds.fast
        slow_min, slow_max = self.bounds.slow
        signal_min, signal_max = self.bounds.signal

        while True:
            fast = self.rng.randint(fast_min, fast_max)
            slow_lower = max(slow_min, fast + self.bounds.min_slow_gap)
            if slow_lower >= slow_max:
                slow_lower = slow_min
            slow = self.rng.randint(slow_lower, slow_max)
            signal = self.rng.randint(signal_min, signal_max)
            params = (fast, slow, signal)
            if params not in self._evaluated:
                return params

    def _propose(self) -> Tuple[int, int, int]:
        X = np.array([self._scale(p) for p in self._x_train])
        y = np.array(self._y_train)

        kernel = ConstantKernel(1.0, (0.1, 10.0)) * Matern(
            length_scale=[1.0, 1.0, 1.0], nu=2.5
        ) + WhiteKernel(noise_level=1e-5)
        gp = GaussianProcessRegressor(
            kernel=kernel,
            normalize_y=True,
            random_state=self.rng.randint(1, 10_000),
            n_restarts_optimizer=3,
            alpha=1e-6,
        )
        gp.fit(X, y)

        candidates: List[Tuple[int, int, int]] = []
        while len(candidates) < self.candidate_pool:
            params = self._sample_random()
            if params not in self._evaluated and params not in candidates:
                candidates.append(params)

        X_cand = np.array([self._scale(p) for p in candidates])
        mu, sigma = gp.predict(X_cand, return_std=True)
        ei = self._expected_improvement(mu, sigma, np.max(y))
        best_idx = int(np.argmax(ei))
        return candidates[best_idx]

    def _expected_improvement(self, mu: np.ndarray, sigma: np.ndarray, best: float) -> np.ndarray:
        epsilon = 1e-6
        sigma = np.maximum(sigma, epsilon)
        improvement = mu - best - 1e-3
        Z = improvement / sigma
        erf_vec = np.vectorize(math.erf)
        cdf = 0.5 * (1.0 + erf_vec(Z / math.sqrt(2.0)))
        pdf = (1.0 / math.sqrt(2.0 * math.pi)) * np.exp(-0.5 * Z * Z)
        ei = improvement * cdf + sigma * pdf
        ei = np.where(sigma <= epsilon, 0.0, ei)
        return ei

    def _scale(self, params: Iterable[int]) -> np.ndarray:
        return np.array(params, dtype=float) / self._scale_vector


__all__ = ["MacdBounds", "MacdSharpeObjective", "BayesianMacdOptimizer"]
