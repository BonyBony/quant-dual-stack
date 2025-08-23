# common/data/yf_loader.py
import pandas as pd
import yfinance as yf

def load_daily(symbol: str, start: str, end: str) -> pd.DataFrame:
    df = yf.download(
        symbol,
        start=start,
        end=end,
        auto_adjust=True,   # adjusted prices
        progress=False,
        actions=False
    )

    if isinstance(df.columns, pd.MultiIndex):
        # yfinance often returns (field, ticker)
        try:
            # Try select the requested symbol explicitly (case-insensitive)
            tickers = df.columns.get_level_values(1)
            # pick the first if only one; otherwise try exact match ignoring case
            pick = next((t for t in tickers.unique() if str(t).lower()==symbol.lower()), tickers.unique()[0])
            df = df.xs(pick, level=1, axis=1)
        except Exception:
            df = df.droplevel(1, axis=1)

    df.columns = [str(c).lower() for c in df.columns]
    # map adj close → close if needed
    if "adj close" in df.columns and "close" not in df.columns:
        df["close"] = df["adj close"]

    # keep only the usuals if they exist
    cols = [c for c in ["open","high","low","close","volume"] if c in df.columns]
    df = df[cols].dropna(how="all").copy()
    # ensure DatetimeIndex is sorted
    df = df.sort_index()
    return df
