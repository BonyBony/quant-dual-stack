import pandas as pd
from typing import List
from strategies.macd import MACDStrategy, MACDParams

def build_macd_labels(df: pd.DataFrame,
                      days: list[pd.Timestamp],
                      param_grid: List[MACDParams]) -> pd.DataFrame:
    strat = MACDStrategy()
    rows = []
    for i in range(len(days) - 1):
        d = days[i]
        d_next = days[i + 1]
        df_next = df.loc[(df.index >= d_next) & (df.index < d_next + pd.Timedelta(days=1))]
        for p in param_grid:
            pnl_next = strat.run_day(df_next, p)
            rows.append({
                "date": d,
                "fast": p.fast,
                "slow": p.slow,
                "signal": p.signal,
                "label": pnl_next
            })
    return pd.DataFrame(rows)
