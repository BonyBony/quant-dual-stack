import pandas as pd
from dataclasses import dataclass

@dataclass(frozen=True)
class MACDParams:
    fast: int
    slow: int
    signal: int

class MACDStrategy:
    """
    Daily-bar MACD:
      • long  when histogram > 0
      • short when histogram < 0
    """
    def run_day(self, df_day: pd.DataFrame, params: MACDParams) -> float:
        if df_day.empty:
            return 0.0

        c = df_day["close"]
        macd   = c.ewm(span=params.fast).mean() - c.ewm(span=params.slow).mean()
        signal = macd.ewm(span=params.signal).mean()
        hist   = macd - signal

        pos = (hist > 0).astype(int) - (hist < 0).astype(int)      # +1 / –1 / 0
        ret = c.pct_change().fillna(0)

        pnl = (pos.shift(1).fillna(0) * ret).sum()
        # ---- FutureWarning fix ----
        if isinstance(pnl, pd.Series):
            pnl = pnl.iloc[0]
        return float(pnl)

    def position(self, df_day: pd.DataFrame, params: MACDParams) -> int:
        """Return the latest position for the provided data slice.

        Parameters
        ----------
        df_day : pd.DataFrame
            Price history up to and including the day of interest.
        params : MACDParams
            Strategy parameters.

        Returns
        -------
        int
            Latest position: +1 for long, -1 for short, 0 for flat.
        """
        if df_day.empty:
            return 0

        c = df_day["close"]
        macd = c.ewm(span=params.fast).mean() - c.ewm(span=params.slow).mean()
        signal = macd.ewm(span=params.signal).mean()
        hist = macd - signal
        pos = (hist > 0).astype(int) - (hist < 0).astype(int)
        return int(pos.iloc[-1]) if not pos.empty else 0
