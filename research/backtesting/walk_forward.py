from __future__ import annotations
from typing import Protocol, Iterable, List, Tuple
import numpy as np
import pandas as pd

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

    def turnover_cost(self, turnover_fraction: float) -> float:
        # cost in return space
        return float(turnover_fraction) * (self.commission_pct + self.slippage_pct)

class WalkForwardBacktester:
    def __init__(self,
                 strategy: Strategy,
                 position_sizer: PositionSizer,
                 stop_loss: StopLoss,
                 cost_model: CostModel,
                 train_window: int = 252,
                 test_window: int = 252,
                 initial_equity: float = 1.0) -> None:
        self.strategy = strategy
        self.position_sizer = position_sizer
        self.stop_loss = stop_loss
        self.cost_model = cost_model
        self.train_window = int(train_window)
        self.test_window = int(test_window)
        self.initial_equity = float(initial_equity)

    def run(self, df: pd.DataFrame, params: Iterable) -> pd.Series:
        """
        Rolling walk-forward:
          • For each train window, pick the MACD param (from `params`)
            with the highest in-sample Sharpe (net costs)
          • Apply that param to the next test window
          • Return a single pd.Series of daily returns named 'return'
        """
        cols = {c.lower() for c in df.columns}
        assert "close" in cols, "df must include 'close' column"
        # normalize column name in case it is 'Close'
        close = df[[c for c in df.columns if c.lower() == "close"][0]].astype(float).values
        idx   = df.index
        n     = len(df)
        if n < (self.train_window + self.test_window + 5):
            return pd.Series(index=idx, data=np.nan, name="return").dropna()

        out_rets: List[pd.Series] = []
        i = self.train_window
        while i + self.test_window <= n:
            tr_slice = slice(i - self.train_window, i)      # [i-train, i)
            te_slice = slice(i, i + self.test_window)       # [i, i+test)
            # 1) pick best param on train
            best_param, _ = self._pick_best(close, idx, tr_slice, params)
            # 2) trade test with that param
            rets_test = self._trade_window(close, idx, te_slice, best_param)
            out_rets.append(rets_test)
            i += self.test_window

        if not out_rets:
            return pd.Series(index=idx, data=np.nan, name="return").dropna()
        rets = pd.concat(out_rets).sort_index()
        rets.name = "return"
        return rets

    # ---------- internals ----------
    def _pick_best(self, close: np.ndarray, idx: pd.Index, win: slice, params: Iterable) -> Tuple[object, float]:
        best_p, best_s = None, -np.inf
        for p in params:
            r = self._trade_window(close, idx, win, p)
            if r.empty or r.std() == 0:
                score = -np.inf
            else:
                score = np.sqrt(252) * r.mean() / r.std()
            if score > best_s:
                best_s, best_p = score, p
        return best_p, best_s

    def _trade_window(self, close: np.ndarray, idx: pd.Index, win: slice, p) -> pd.Series:
        """
        Simple daily engine:
          • Position = strategy.position(history up to t, p)
          • Stop-loss evaluated on close-to-close (daily approx)
          • Costs applied on position changes (turnover)
        Returns daily returns for the window index.
        """
        start, end = win.start, win.stop
        if end - start < 2:
            return pd.Series(index=idx[start:end], data=0.0)

        pos = 0
        entry_price = None
        prev_price = float(close[start])
        size = float(self.position_sizer.risk_per_trade)  # interpret as notional fraction
        rets = np.zeros(end - start, dtype=float)

        def _pos_at(day_i: int) -> int:
            hist = pd.DataFrame({"close": close[:day_i+1]}, index=idx[:day_i+1])
            try:
                return int(self.strategy.position(hist, p))
            except Exception:
                return 0

        for k, t in enumerate(range(start, end)):
            price = float(close[t])
            new_pos = _pos_at(t)

            # transaction cost on turnover
            turnover = abs(new_pos - pos) * size
            cost = self.cost_model.turnover_cost(turnover)

            if pos == 0 and new_pos != 0:
                entry_price = price
                pos = new_pos
                rets[k] = -cost
            elif pos != 0:
                # daily pnl from prior position
                ret = pos * size * ((price - prev_price) / prev_price)
                # stop loss check (approximated on close)
                if self.stop_loss.hit(entry_price, price, pos):
                    new_pos = 0
                if new_pos != pos:
                    # apply cost on exit/flip
                    ret -= cost
                    if new_pos != 0:
                        entry_price = price
                pos = new_pos
                rets[k] = ret
            else:
                rets[k] = 0.0

            prev_price = price

        s = pd.Series(rets, index=idx[start:end], name="return")
        return s
