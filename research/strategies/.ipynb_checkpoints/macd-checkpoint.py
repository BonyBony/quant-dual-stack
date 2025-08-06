import pandas as pd
from dataclasses import dataclass

@dataclass(frozen=True)
class MACDParams:
    fast: int
    slow: int
    signal: int

class MACDStrategy:
    def run_day(self, df_day: pd.DataFrame, params: MACDParams) -> float:
        if df_day.empty:
            return 0.0
        c = df_day['close']
        macd = c.ewm(span=params.fast).mean() - c.ewm(span=params.slow).mean()
        signal = macd.ewm(span=params.signal).mean()
        hist = macd - signal
        pos = (hist > 0).astype(int) - (hist < 0).astype(int)
        ret = c.pct_change().fillna(0)
        pnl = (pos.shift(1).fillna(0) * ret).sum()
        return float(pnl)
