from __future__ import annotations

"""Walk-forward backtesting utilities with risk and cost modelling.

This module provides a minimal yet extensible backtesting framework that is
compatible with the existing research pipeline.  It supports:

* walk-forward evaluation using a rolling train/test window
* position sizing
* stop-loss handling
* transaction cost and slippage simulation

The design follows SOLID principles by separating responsibilities across
small data classes.
"""

from dataclasses import dataclass
from typing import Iterable, Protocol
import pandas as pd


class Strategy(Protocol):
    """Protocol for strategies used by the backtester."""

    def position(self, df: pd.DataFrame, params: object) -> int:
        """Return the latest position for the provided data slice."""


@dataclass(frozen=True)
class PositionSizer:
    """Fixed-fractional position sizing."""

    risk_per_trade: float

    def size(self, equity: float, price: float) -> float:
        return (equity * self.risk_per_trade) / price


@dataclass(frozen=True)
class StopLoss:
    """Simple percentage stop loss."""

    pct: float

    def hit(self, entry: float, current: float, side: int) -> bool:
        if side > 0:
            return (current - entry) / entry <= -self.pct
        if side < 0:
            return (entry - current) / entry <= -self.pct
        return False


@dataclass(frozen=True)
class CostModel:
    """Linear transaction cost and slippage model."""

    commission_pct: float = 0.0
    slippage_pct: float = 0.0

    def cost(self, price: float, size: float) -> float:
        trade_val = price * size
        return trade_val * (self.commission_pct + self.slippage_pct)


@dataclass
class WalkForwardBacktester:
    """Walk-forward backtesting engine.

    Parameters
    ----------
    strategy : Strategy
        Trading strategy implementing the :class:`Strategy` protocol.
    position_sizer : PositionSizer
        Determines number of shares/contracts to trade.
    stop_loss : StopLoss
        Stop-loss rule applied to open positions.
    cost_model : CostModel
        Transaction cost and slippage model.
    train_window : int, default 252
        Number of bars used for in-sample training.
    test_window : int, default 252
        Number of bars evaluated out-of-sample.
    initial_equity : float, default 1.0
        Starting account equity.
    """

    strategy: Strategy
    position_sizer: PositionSizer
    stop_loss: StopLoss
    cost_model: CostModel
    train_window: int = 252
    test_window: int = 252
    initial_equity: float = 1.0

    def run(self, df: pd.DataFrame, params: Iterable) -> pd.Series:
        """Run walk-forward backtest over ``df`` starting in 2019.

        Parameters
        ----------
        df : pd.DataFrame
            Price history with at least a ``close`` column and a ``DatetimeIndex``.
        params : Iterable
            Iterable of strategy parameter objects aligned with test periods.

        Returns
        -------
        pd.Series
            Equity curve indexed by test period end dates.
        """

        df = df.loc[df.index >= pd.Timestamp("2019-01-01")]
        days = df.index
        equity = self.initial_equity
        equity_curve = []
        idx = []
        pos = 0
        entry_price = 0.0
        size = 0.0
        params_iter = iter(params)

        for i in range(self.train_window, len(days)):
            d = days[i]
            hist = df.iloc[: i + 1]
            price = hist["close"].iloc[-1]
            prev_price = hist["close"].iloc[-2]
            p = next(params_iter, None)
            p = p if p is not None else params  # handle single param

            new_pos = self.strategy.position(hist, p)

            if pos == 0 and new_pos != 0:
                size = self.position_sizer.size(equity, price)
                cost = self.cost_model.cost(price, size)
                equity -= cost
                entry_price = price
                pos = new_pos
            elif pos != 0:
                ret = (price - prev_price) / prev_price
                if self.stop_loss.hit(entry_price, price, pos):
                    new_pos = 0
                equity += pos * size * ret
                if new_pos != pos:
                    cost = self.cost_model.cost(price, size)
                    equity -= cost
                    if new_pos != 0:
                        entry_price = price
                        size = self.position_sizer.size(equity, price)
                pos = new_pos
            equity_curve.append(equity)
            idx.append(d)

        return pd.Series(equity_curve, index=idx)
