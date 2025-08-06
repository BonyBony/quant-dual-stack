import pandas as pd
from typing import List
from research.strategies.macd import MACDStrategy, MACDParams

def build_macd_labels(df: pd.DataFrame, days: list[pd.Timestamp], param_grid: List[MACDParams]) -> pd.DataFrame:
    strat = MACDStrategy()
    rows = []
    max_slow = max([p.slow for p in param_grid])
    for i in range(max_slow, len(days) - 1):
        d = days[i]
        d_next = days[i + 1]
        # Get at least `max_slow` bars up to d_next (plus one extra for signal)
        df_slice = df.loc[df.index <= d_next].tail(max_slow + 2)
        if df_slice.empty or len(df_slice) < max_slow:
            continue
        for p in param_grid:
            pnl_next = strat.run_day(df_slice, p)
            rows.append({"date": d, **p.__dict__, "label": pnl_next})
    return pd.DataFrame(rows)
