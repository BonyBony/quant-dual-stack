import pandas as pd
import yfinance as yf

def load_daily(symbol: str, start: str, end: str) -> pd.DataFrame:
    df = yf.download(symbol, start=start, end=end, auto_adjust=True, progress=False)
    if df.empty:
        raise ValueError(f"No data for {symbol}")
    df = df.rename(columns=str.lower)
    df.index = pd.to_datetime(df.index)
    return df

def load_pair_daily(primary: str, hedge: str, start: str, end: str) -> pd.DataFrame:
    df = yf.download([primary, hedge], start=start, end=end, auto_adjust=True, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        close = df['Adj Close'] if 'Adj Close' in df.columns.levels[0] else df['Close']
    else:
        close = df[['Close']]
    close = close.dropna()
    close.columns = [c.upper() for c in close.columns]
    return close
