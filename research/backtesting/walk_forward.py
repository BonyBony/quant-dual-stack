# research/backtesting/walk_forward.py
from __future__ import annotations
from typing import Protocol, Iterable, List, Tuple, Dict, Optional
from dataclasses import dataclass
import numpy as np
import pandas as pd

# --- Optional numba accel (safe fallback if unavailable) ---
try:
    from numba import njit
except Exception:  # numba not installed
    def njit(*args, **kwargs):
        def deco(f):
            return f
        return deco

class Strategy(Protocol):
    def position(self, df_slice: pd.DataFrame, params) -> int: ...

class PositionSizer:
    """Fixed fractional ‘risk per trade’ / notional fraction."""
    def __init__(self, risk_per_trade: float):
        self.risk_per_trade = float(risk_per_trade)

class StopLoss:
    """Simple percentage stop on daily bars (close/close approximation)."""
    def __init__(self, pct: float):
        self.pct = float(pct)

    def _scalar(self, x) -> float:
        if hasattr(x, "item"):
            try:
                return x.item()  # numpy/pandas 0-d
            except Exception:
                pass
        try:
            arr = np.asarray(x)
            return float(arr.reshape(-1)[-1])
        except Exception:
            return float(x)

    def hit(self, entry_price, price, pos) -> bool:
        e = self._scalar(entry_price)
        p = self._scalar(price)
        s = int(pos)
        if s > 0:
            return p <= e * (1.0 - self.pct)
        if s < 0:
            return p >= e * (1.0 + self.pct)
        return False

class CostModel:
    """Linear costs applied on notional turnover (abs change in position * fraction)."""
    def __init__(self, commission_pct: float = 0.0, slippage_pct: float = 0.0):
        self.commission_pct = float(commission_pct)
        self.slippage_pct  = float(slippage_pct)

    @property
    def rate(self) -> float:
        return self.commission_pct + self.slippage_pct

    def turnover_cost(self, turnover_fraction: float | np.ndarray) -> float | np.ndarray:
        return self.rate * turnover_fraction

@dataclass
class WalkForwardBacktester:
    strategy: Strategy
    position_sizer: PositionSizer
    stop_loss: StopLoss
    cost_model: CostModel
    train_window: int = 252
    test_window: int = 252
    initial_equity: float = 1.0

    # cache of positions for each (fast,slow,signal) -> np.ndarray of int8
    pos_cache: Optional[Dict[Tuple[int,int,int], np.ndarray]] = None
    # speed knob: ignore stop during train selection
    fast_train: bool = True

    def run(self, df: pd.DataFrame, params: Iterable) -> pd.Series:
        cols = {c.lower() for c in df.columns}
        assert "close" in cols, "df must include 'close' column"
        close_col = [c for c in df.columns if c.lower() == "close"][0]
        close = df[close_col].astype(float).to_numpy()
        idx   = df.index
        n     = len(df)
        if n < (self.train_window + self.test_window + 5):
            return pd.Series(index=idx, data=np.nan, name="return").dropna()

        # Precompute close-to-close returns once
        ret = np.zeros(n, dtype=np.float64)
        ret[1:] = (close[1:] - close[:-1]) / close[:-1]

        # Build cache once if missing
        if self.pos_cache is None:
            # materialize params (in case it's a generator)
            grid = list(params)
            from research.strategies.macd import MACDParams, precompute_macd_positions
            self.pos_cache = precompute_macd_positions(df, grid)
            params = grid
        else:
            params = list(params)

        out_rets: List[pd.Series] = []
        i = self.train_window
        while i + self.test_window <= n:
            tr = slice(i - self.train_window, i)    # [i-train, i)
            te = slice(i, i + self.test_window)     # [i, i+test)

            best_param, _ = self._pick_best_cached(ret, tr, params)
            rets_test = self._trade_test_with_stop(idx, close, te, best_param)
            out_rets.append(rets_test)
            i += self.test_window

        if not out_rets:
            return pd.Series(index=idx, data=np.nan, name="return").dropna()
        rets = pd.concat(out_rets).sort_index()
        rets.name = "return"
        return rets

    # ---------- internals ----------
    def _pos_series(self, p) -> np.ndarray:
        key = (int(p.fast), int(p.slow), int(p.signal))
        return self.pos_cache[key].astype(np.int16)

    def _pick_best_cached(self, ret: np.ndarray, win: slice, params: Iterable) -> Tuple[object, float]:
        """Fast train selection: vectorized PnL + turnover costs; no stop."""
        s, e = win.start, win.stop
        r = ret[s:e]
        best_p, best_s = None, -np.inf
        size = float(self.position_sizer.risk_per_trade)
        rate = float(self.cost_model.rate)

        for p in params:
            pos = self._pos_series(p)[s:e]
            if len(pos) < 2:
                continue
            # decisions at t → return from t→t+1
            pnl = (pos[:-1] * r[1:]) * size
            turn = np.abs(np.diff(pos)) * size
            cost = turn * rate
            pnl = pnl - cost
            sd = pnl.std()
            if pnl.size == 0 or sd == 0 or not np.isfinite(sd):
                score = -np.inf
            else:
                score = np.sqrt(252.0) * pnl.mean() / sd
            if score > best_s:
                best_s, best_p = score, p
        return best_p, best_s

    def _trade_test_with_stop(self, idx: pd.Index, close: np.ndarray, win: slice, p) -> pd.Series:
        """Simulate test window using cached positions for chosen param, with stop."""
        s, e = win.start, win.stop
        pos = self._pos_series(p)
        size = float(self.position_sizer.risk_per_trade)
        rate = float(self.cost_model.rate)
        stop = float(self.stop_loss.pct)

        rets = _simulate_test_with_stop(close, pos, s, e, stop, size, rate)
        return pd.Series(rets, index=idx[s:e], name="return")

@njit(cache=True)
def _simulate_test_with_stop(close: np.ndarray,
                             pos: np.ndarray,
                             start: int,
                             end:   int,
                             stop_pct: float,
                             size: float,
                             cost_rate: float) -> np.ndarray:
    out = np.zeros(end - start, dtype=np.float64)
    pos_prev = 0
    entry_price = 0.0

    for k, t in enumerate(range(start, end)):
        price = close[t]
        new_pos = int(pos[t])
        turn = abs(new_pos - pos_prev) * size
        daily_cost = turn * cost_rate

        if pos_prev == 0 and new_pos != 0:
            entry_price = price
            pos_prev = new_pos
            out[k] = -daily_cost
        elif pos_prev != 0:
            r = 0.0
            if t + 1 < close.shape[0]:
                r = (close[t+1] - close[t]) / close[t]

            # stop check on close
            if pos_prev > 0 and price <= entry_price * (1.0 - stop_pct):
                new_pos = 0
            elif pos_prev < 0 and price >= entry_price * (1.0 + stop_pct):
                new_pos = 0

            pnl = pos_prev * size * r
            if new_pos != pos_prev:
                pnl -= daily_cost
                if new_pos != 0:
                    entry_price = price
            pos_prev = new_pos
            out[k] = pnl
        else:
            out[k] = 0.0

    return out
