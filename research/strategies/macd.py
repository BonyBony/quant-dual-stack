from dataclasses import dataclass
import pandas as pd


@dataclass(frozen=True)
class MACDParams:
    fast: int
    slow: int
    signal: int


class MACDStrategy:
    """
    Minimal daily-bar MACD strategy with an optional 'deadband' gate:
    - Uses EMA (adjust=False) for MACD.
    - If |histogram_t| < deadband_threshold, return FLAT (0) to avoid
      whipsaws smaller than your round-trip cost (commission+slippage).
    """

    def __init__(self, deadband_threshold: float = 0.0) -> None:
        # Interpreted in the same scale as price differences (MACD histogram).
        # You can set/override this after construction:
        #   strat.deadband_threshold = commission_pct + slippage_pct
        self.deadband_threshold = float(deadband_threshold)

    def run_day(self, df_day: pd.DataFrame, params: MACDParams) -> float:
        """PnL over df_day (daily bars), using MACD histogram sign."""
        if df_day.empty:
            return 0.0
        c = df_day["close"].astype(float)
        macd = c.ewm(span=params.fast, adjust=False).mean() - c.ewm(
            span=params.slow, adjust=False
        ).mean()
        signal = macd.ewm(span=params.signal, adjust=False).mean()
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
        macd = c.ewm(span=params.fast, adjust=False).mean() - c.ewm(
            span=params.slow, adjust=False
        ).mean()
        signal = macd.ewm(span=params.signal, adjust=False).mean()
        hist = macd - signal

        # Deadband gate: ignore tiny signals (set from costs)
        thr = getattr(self, "deadband_threshold", 0.0)
        if len(hist) == 0:
            return 0
        if abs(float(hist.iat[-1])) < float(thr):
            return 0

        pos = (hist > 0).astype(int) - (hist < 0).astype(int)
        return int(pos.iat[-1]) if len(pos) else 0
