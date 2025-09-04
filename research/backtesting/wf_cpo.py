from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Tuple
import json
from pathlib import Path

import numpy as np
import pandas as pd

from common.data.yf_loader import load_daily
from common.features.chan_ex7_1_daily import compute_features_daily

from research.strategies.macd import MACDParams, MACDStrategy
from research.backtesting.walk_forward import PositionSizer, StopLoss, CostModel
from research.cpo.engine import (
    build_param_grid, build_training_table, fit_cpo_model, select_params_for_day
)


@dataclass
class WF_CPO_Config:
    symbol: str
    train_start: str
    train_end: str
    test_start: str
    test_end: str
    macd_grid: Dict
    lookbacks: List[int]
    model_name: str = "hgbt"
    n_splits: int = 5
    embargo_groups: int = 1
    artifacts_dir: str = "research/artifacts/macd_cpo"


class WF_CPOBacktester:
    """
    Walk-forward with CPO:
      • Train leakage-safe model on train window
      • In OOS, at each day t, select params via model(feats_t, grid) -> argmax
      • Trade next-day close→close using MACD & apply costs/stops
    """

    def __init__(
        self,
        position_sizer: PositionSizer,
        stop_loss: StopLoss,
        cost_model: CostModel,
    ):
        self.sizer = position_sizer
        self.stop = stop_loss
        self.cost = cost_model

    def _day_ret_with_costs(
        self, closes: pd.Series, pos_prev: int, pos_new: int, i: int
    ) -> float:
        """
        Return for move from day i to i+1 given previous pos and new pos decisions @ day i.
        - PnL from exposure 'pos_prev' over close[i]→close[i+1].
        - Transaction cost on turnover abs(pos_new - pos_prev) * notional fraction.
        """
        ret_ip1 = (closes.iloc[i + 1] - closes.iloc[i]) / closes.iloc[i]
        turnover = abs(pos_new - pos_prev) * self.sizer.risk_per_trade
        cost = self.cost.turnover_cost(turnover)
        pnl = pos_prev * self.sizer.risk_per_trade * ret_ip1 - cost
        return float(pnl)

    def run(self, cfg: WF_CPO_Config) -> Tuple[pd.Series, pd.DataFrame]:
        # 1) Load data
        df = load_daily(cfg.symbol, cfg.train_start, cfg.test_end).copy()
        # tolerate both single-index and multi-index columns
        if isinstance(df.columns, pd.MultiIndex):
            df = df.copy()
            df.columns = [c[0].lower() for c in df.columns]
        else:
            df = df.rename(columns=str.lower)
        close = df["close"].astype(float)

        # 2) Param grid
        pg, pg_dicts = build_param_grid(cfg.macd_grid)

        # 3) Days
        days = pd.to_datetime(df.index)
        train_days = days[
            (days >= pd.Timestamp(cfg.train_start)) & (days <= pd.Timestamp(cfg.train_end))
        ]
        test_days = days[
            (days >= pd.Timestamp(cfg.test_start)) & (days <= pd.Timestamp(cfg.test_end))
        ]

        # 4) Build training table & fit model (purged CV inside engine)
        X, y, groups, max_slow = build_training_table(
            df, train_days, pg, cfg.lookbacks, self.cost
        )
        model, report = fit_cpo_model(
            X, y, groups, cfg.n_splits, cfg.embargo_groups, cfg.model_name
        )

        # 5) OOS: daily param selection and trading
        strat = MACDStrategy()
        # cost-aware deadband: ignore MACD histogram signals smaller than round-trip cost
        round_trip_cost = float(self.cost.commission_pct + self.cost.slippage_pct)
        strat.deadband_threshold = round_trip_cost

        pos_prev = 0
        entry_price: float | None = None
        rets: List[float] = []
        dates: List[pd.Timestamp] = []

        # ensure we have enough history to start decisions
        start_idx = close.index.get_loc(test_days[0])
        i = max(start_idx, max_slow)  # index in close

        while i + 1 < len(close) and close.index[i] <= test_days[-1]:
            d = close.index[i]

            # features as of day d (no peeking)
            feats_today = compute_features_daily(df.loc[:d], cfg.lookbacks)
            best = select_params_for_day(model, feats_today, pg_dicts)
            p = MACDParams(**best)

            # today's decision (applies from next bar)
            hist_i = pd.DataFrame({"close": close.iloc[: i + 1]}, index=close.index[: i + 1])
            pos_new = strat.position(hist_i, p)

            # stop-loss check on today's open exposure over close→close
            if pos_prev != 0 and entry_price is not None:
                next_close = float(close.iloc[i + 1])
                if self.stop.hit(entry_price, next_close, pos_prev):
                    pos_new = 0  # flatten for next day

            # compute today's PnL & costs using current exposure
            pnl = self._day_ret_with_costs(close, pos_prev, pos_new, i)
            rets.append(pnl)
            dates.append(close.index[i + 1])

            # update state for tomorrow
            if pos_prev == 0 and pos_new != 0:
                # entering at today's close for next-day exposure
                entry_price = float(close.iloc[i])
            elif pos_new == 0:
                entry_price = None
            pos_prev = pos_new
            i += 1

        rets = pd.Series(rets, index=pd.DatetimeIndex(dates), name="return")

        # 6) Save CV meta
        art = Path(cfg.artifacts_dir)
        art.mkdir(parents=True, exist_ok=True)
        meta = {
            "cv_rmse_mean": report.rmse_mean,
            "cv_rmse_std": report.rmse_std,
            "splits": report.splits,
            "embargo_groups": report.embargo_groups,
        }
        with open(art / "cpo_cv_report.json", "w") as f:
            json.dump(meta, f, indent=2)

        # Return OOS returns + training table for quick introspection
        return rets, X
