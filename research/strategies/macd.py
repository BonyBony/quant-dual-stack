from dataclasses import dataclass
import pandas as pd

@dataclass(frozen=True)
class MACDParams:
    fast: int
    slow: int
    signal: int

class MACDStrategy:
    def run_day(self, df_day: pd.DataFrame, params: MACDParams) -> float:
        """PnL over df_day (daily bars), using MACD histogram sign."""
        if df_day.empty:
            return 0.0
        c = df_day["close"].astype(float)
        macd = c.ewm(span=params.fast).mean() - c.ewm(span=params.slow).mean()
        signal = macd.ewm(span=params.signal).mean()
        hist = macd - signal
        pos = (hist > 0).astype(int) - (hist < 0).astype(int)
        ret = c.pct_change().fillna(0.0)
        pnl = (pos.shift(1).fillna(0.0) * ret).sum()
        return float(pnl)

    def position(self, df_hist: pd.DataFrame, params: MACDParams) -> int:
        """
        Position at the last bar of df_hist:
          +1 long, -1 short, 0 flat
        """
        if df_hist.empty:
            return 0
        c = df_hist["close"].astype(float)
        macd = c.ewm(span=params.fast).mean() - c.ewm(span=params.slow).mean()
        signal = macd.ewm(span=params.signal).mean()
        hist = macd - signal
        pos = (hist > 0).astype(int) - (hist < 0).astype(int)
        # scalar-safe (avoid FutureWarning on int(Series))
        return int(pos.iat[-1]) if len(pos) else 0
