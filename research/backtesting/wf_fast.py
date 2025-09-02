from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Dict, Iterable, Tuple, List

import numpy as np
import pandas as pd

from research.strategies.macd import MACDParams  # frozen dataclass (hashable)
from common.utils.stats import get_return_metrics


# ----------------------------- helpers ---------------------------------

def _flatten_ohlc(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure lower-case, single-level columns with `close` present."""
    out = df.copy()
    if isinstance(out.columns, pd.MultiIndex):
        out.columns = [str(c[0]).lower() for c in out.columns]
    else:
        out.columns = [str(c).lower() for c in out.columns]
    if "close" not in out.columns:
        raise ValueError(f"'close' column missing; got {out.columns.tolist()}")
    return out


def _macd_sign_array(close_s: pd.Series, p: MACDParams) -> np.ndarray:
    """Return +1/-1/0 MACD histogram sign as int8 array for one parameter set."""
    ema_f = close_s.ewm(span=p.fast, adjust=False).mean()
    ema_s = close_s.ewm(span=p.slow, adjust=False).mean()
    macd = ema_f - ema_s
    signal = macd.ewm(span=p.signal, adjust=False).mean()
    hist = macd - signal
    out = np.zeros(len(hist), dtype=np.int8)
    v = hist.to_numpy()
    out[v > 0] = 1
    out[v < 0] = -1
    return out


# --------------------- public: preparation step -------------------------

@dataclass(frozen=True)
class WFInputs:
    """Prepared inputs for fast walk-forward."""
    close: pd.Series             # clean, lower-case, single-index
    rets: np.ndarray             # daily returns (close.pct_change, NaN->0)
    dates: pd.DatetimeIndex      # close.index
    sign_cache: Dict[MACDParams, np.ndarray]  # MACD sign per parameter


def prepare_wf_inputs(
    df: pd.DataFrame,
    params: Iterable[MACDParams],
) -> WFInputs:
    """
    Clean price data and precompute all MACD sign series once.

    Parameters
    ----------
    df : DataFrame with OHLC, DatetimeIndex
    params : iterable of MACDParams

    Returns
    -------
    WFInputs
    """
    px = _flatten_ohlc(df)
    close = px["close"].astype(float)
    rets = close.pct_change().fillna(0.0).to_numpy()
    dates = close.index
    # precompute signs for each parameter
    sign_cache = {p: _macd_sign_array(close, p) for p in params}
    return WFInputs(close=close, rets=rets, dates=dates, sign_cache=sign_cache)


# ----------------- internal fast engines (array based) ------------------

def _trade_window_with_cost_stop(
    close_arr: np.ndarray,
    sign: np.ndarray,
    rets: np.ndarray,
    start: int,
    end: int,
    stop_pct: float,
    cost_rate: float,   # commission+slippage as fraction (bps / 1e4)
) -> np.ndarray:
    """
    Simulate daily returns on [start, end) for a given sign path.
    - Position changes charged at `cost_rate` (turnover in notional units).
    - Stop evaluated on close/close (daily approximation).
    - Notional fraction = 1.0 (returns are already fractions).

    Returns float array of length end-start.
    """
    n = end - start
    if n <= 0:
        return np.zeros(0, dtype=float)

    out = np.zeros(n, dtype=float)

    pos_prev = 0          # last position (-1/0/+1)
    entry_price = np.nan  # last entry price for stop check

    for k, t in enumerate(range(start, end)):
        pos_new = int(sign[t])
        price_t = float(close_arr[t])

        # turnover cost (0 if no change, cost_rate if open/close, 2* if flip)
        turnover = abs(pos_new - pos_prev)
        cost = turnover * cost_rate

        if pos_prev == 0 and pos_new != 0:
            # open position at today's close
            entry_price = price_t
            out[k] = -cost
            pos_prev = pos_new
            continue

        if pos_prev != 0:
            # daily pnl from prior position using returns array
            day_ret = float(rets[t])

            # stop on close/close if enabled
            if stop_pct > 0.0 and not np.isnan(entry_price):
                if pos_prev > 0 and price_t <= entry_price * (1.0 - stop_pct):
                    # stop-out on long
                    out[k] = pos_prev * day_ret - cost
                    pos_prev = 0
                    entry_price = np.nan
                    continue
                if pos_prev < 0 and price_t >= entry_price * (1.0 + stop_pct):
                    # stop-out on short
                    out[k] = pos_prev * day_ret - cost
                    pos_prev = 0
                    entry_price = np.nan
                    continue

            # no stop; apply pnl and handle change
            if pos_new != pos_prev:
                # pay cost when we change
                out[k] = pos_prev * day_ret - cost
                if pos_new != 0:
                    entry_price = price_t
            else:
                out[k] = pos_prev * day_ret

        pos_prev = pos_new

    return out


def _pick_best_param_on_train(
    sign_cache: Dict[MACDParams, np.ndarray],
    close_arr: np.ndarray,
    rets: np.ndarray,
    start: int,
    end: int,
    stop_pct: float,
    cost_rate: float,
) -> Tuple[MACDParams, float]:
    """Return (best_param, best_sharpe) by in-sample Sharpe on [start, end)."""
    best_p, best_s = None, -np.inf
    for p, sign in sign_cache.items():
        r = _trade_window_with_cost_stop(close_arr, sign, rets, start, end, stop_pct, cost_rate)
        if r.size < 2 or r.std() == 0:
            s = -np.inf
        else:
            s = (r.mean() / r.std()) * sqrt(252.0)
        if s > best_s:
            best_s, best_p = s, p
    return best_p, best_s


# ---------------------- public: fast walk-forward -----------------------

def run_walk_forward_fast(
    inputs: WFInputs,
    train_window: int,
    test_window: int,
    stop_pct: float,
    cost_rate: float,
) -> pd.Series:
    """
    Rolling walk-forward:
      • Pick best MACD params on each train window (Sharpe net of costs)
      • Trade next test window using that param
      • Return a single pd.Series of daily OOS returns (name='return')
    """
    close, rets, dates, sign_cache = inputs.close, inputs.rets, inputs.dates, inputs.sign_cache
    n = len(rets)
    out: List[pd.Series] = []

    i = train_window
    while i + test_window <= n:
        tr_s, tr_e = i - train_window, i
        te_s, te_e = i, i + test_window

        p_best, _ = _pick_best_param_on_train(sign_cache, close.values, rets, tr_s, tr_e, stop_pct, cost_rate)
        sign = sign_cache[p_best]
        r_te = _trade_window_with_cost_stop(close.values, sign, rets, te_s, te_e, stop_pct, cost_rate)
        if r_te.size:
            out.append(pd.Series(r_te, index=dates[te_s:te_e], name="return"))
        i += test_window

    if not out:
        return pd.Series(dtype=float, name="return")
    return pd.concat(out)


# ------------------------ public: grid sweep ----------------------------

def run_cost_stop_sweep_fast(
    inputs: WFInputs,
    commission_bps_list=(0, 5, 10),
    slippage_bps_list=(0, 5, 10),
    stop_list=(0.01, 0.015, 0.02, 0.03),
    train_years: int = 3,
    test_months: int = 6,
) -> pd.DataFrame:
    """
    Sweep across (commission_bps, slippage_bps, stop_pct).
    Returns a tidy DataFrame with standard return metrics.
    """
    rows = []
    train_window = int(252 * train_years)
    test_window = int(21 * test_months)

    for cbps in commission_bps_list:
        for sbps in slippage_bps_list:
            cost_rate = (cbps + sbps) / 10000.0  # bps → fraction
            for stop in stop_list:
                rets_oos = run_walk_forward_fast(
                    inputs,
                    train_window=train_window,
                    test_window=test_window,
                    stop_pct=stop,
                    cost_rate=cost_rate,
                ).dropna()

                if rets_oos.empty or rets_oos.std() == 0:
                    metrics = {"n": 0, "mean": 0, "std": 0, "sharpe": 0, "cagr": 0, "max_dd": 0, "win_rate": 0}
                else:
                    metrics = get_return_metrics(rets_oos)

                rows.append({
                    "commission_bps": cbps,
                    "slippage_bps": sbps,
                    "stop_pct": stop,
                    **metrics,
                })

    return pd.DataFrame(rows)
