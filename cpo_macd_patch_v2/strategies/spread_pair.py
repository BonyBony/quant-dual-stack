import pandas as pd
import numpy as np
from dataclasses import dataclass
from .base import IStrategy, BaseParams
import statsmodels.api as sm

@dataclass(frozen=True)
class SpreadParams(BaseParams):
    entry_threshold: float
    lookback: int
    beta_mode: str = "ols"

class SpreadPairStrategy(IStrategy):
    def __init__(self, primary: str, hedge: str):
        self.primary = primary
        self.hedge = hedge

    def _calc_beta(self, y: pd.Series, x: pd.Series) -> float:
        X = sm.add_constant(x)
        return sm.OLS(y, X).fit().params[1]

    def run_day(self, df_day: pd.DataFrame, params: SpreadParams) -> float:
        return 0.0

    def run_series(self, df: pd.DataFrame, params: SpreadParams) -> pd.Series:
        y = np.log(df[self.primary])
        x = np.log(df[self.hedge])
        beta = self._calc_beta(y, x)
        spread = y - beta * x
        ema = spread.ewm(span=params.lookback).mean()
        var = (spread - ema).pow(2).ewm(span=params.lookback).mean()
        z = (spread - ema) / np.sqrt(var)

        entry_th = params.entry_threshold
        exit_th = -0.6 * entry_th

        pos = pd.Series(0, index=df.index)
        pos[z < -entry_th] = 1
        pos[z >  entry_th] = -1
        pos[(pos.shift(1) == 1) & (z > exit_th)] = 0
        pos[(pos.shift(1) == -1) & (z < -exit_th)] = 0
        pos = pos.ffill().fillna(0)

        ret_p = df[self.primary].pct_change().fillna(0)
        ret_h = df[self.hedge].pct_change().fillna(0)
        pnl = pos.shift(1).fillna(0) * ret_p - pos.shift(1).fillna(0) * beta * ret_h
        return pnl
