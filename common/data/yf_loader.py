# common/data/yf_loader.py
from __future__ import annotations

import pandas as pd
import yfinance as yf
import requests

try:  # yfinance exposes the error in newer releases
    from yfinance.shared._exceptions import YFTzMissingError
except Exception:  # pragma: no cover - older yfinance versions
    YFTzMissingError = Exception  # type: ignore

NSE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.nseindia.com/",
    "Connection": "keep-alive",
    "Host": "www.nseindia.com",
    "sec-ch-ua": '"Chromium";v="124", "Not.A/Brand";v="8", "Google Chrome";v="124"',
    "sec-ch-ua-platform": '"Windows"',
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-fetch-dest": "empty",
    "x-requested-with": "XMLHttpRequest",
    "pragma": "no-cache",
    "cache-control": "no-cache",
}

def load_daily(symbol: str, start: str, end: str) -> pd.DataFrame:
    """Download daily OHLCV, falling back to NSE if Yahoo lacks metadata."""

    def _normalize(df_raw: pd.DataFrame) -> pd.DataFrame:
        df = df_raw.copy()
        if isinstance(df.columns, pd.MultiIndex):
            try:
                tickers = df.columns.get_level_values(1)
                pick = next(
                    (t for t in tickers.unique() if str(t).lower() == symbol.lower()),
                    tickers.unique()[0],
                )
                df = df.xs(pick, level=1, axis=1)
            except Exception:
                df = df.droplevel(1, axis=1)

        df.columns = [str(c).lower() for c in df.columns]
        if "adj close" in df.columns and "close" not in df.columns:
            df["close"] = df["adj close"]
        cols = [c for c in ["open", "high", "low", "close", "volume"] if c in df.columns]
        df = df[cols].dropna(how="all").copy()
        df = df.sort_index()
        return df

    def _download_yf() -> pd.DataFrame:
        out = yf.download(
        symbol,
        start=start,
        end=end,
        auto_adjust=True,   # adjusted prices
        progress=False,
        actions=False
    )
        return out

    def _download_nse() -> pd.DataFrame:
        sym = symbol.replace(".NS", "").upper()
        start_dt = pd.Timestamp(start).date()
        end_dt = pd.Timestamp(end).date()

        archive_headers = {
            "User-Agent": NSE_HEADERS["User-Agent"],
            "Accept": "application/zip,application/octet-stream",
            "Referer": "https://www.nseindia.com/",
        }

        frames = []
        for day in pd.date_range(start_dt, end_dt, freq="D"):
            month = day.strftime("%b").upper()
            url = (
                "https://archives.nseindia.com/content/historical/EQUITIES/"
                f"{day.year}/{month}/cm{day.strftime('%d%b%Y').upper()}bhav.csv.zip"
            )
            try:
                resp = requests.get(url, headers=archive_headers, timeout=10)
                if resp.status_code != 200:
                    continue
                from io import BytesIO
                from zipfile import ZipFile

                with ZipFile(BytesIO(resp.content)) as zf:
                    name = zf.namelist()[0]
                    with zf.open(name) as fh:
                        day_df = pd.read_csv(fh)
            except Exception:
                continue

            day_df = day_df.loc[day_df.get("SYMBOL") == sym]
            if day_df.empty:
                continue
            row = day_df.iloc[0]
            frames.append(
                {
                    "date": pd.to_datetime(row.get("TIMESTAMP")),
                    "open": float(row.get("OPEN", float("nan"))),
                    "high": float(row.get("HIGH", float("nan"))),
                    "low": float(row.get("LOW", float("nan"))),
                    "close": float(row.get("CLOSE", float("nan"))),
                    "volume": float(row.get("TOTTRDQTY", float("nan"))),
                }
            )

        if not frames:
            return pd.DataFrame()
        df = pd.DataFrame(frames).dropna(subset=["date"])
        df = df.set_index("date").sort_index()
        return df

    def _needs_fallback(err: Exception) -> bool:
        msg = str(err).lower()
        return isinstance(err, YFTzMissingError) or "no timezone" in msg or "possibly delisted" in msg

    try:
        raw = _download_yf()
        if raw.empty:
            raise ValueError("empty dataframe")
        df = _normalize(raw)
        if df.empty:
            raise ValueError("empty dataframe after normalize")
        return df
    except Exception as err:
        if not _needs_fallback(err):
            raise

    # --- NSE fallback -------------------------------------------------
    df_nse = _download_nse()
    if df_nse.empty:
        raise RuntimeError(f"Fallback NSE download failed for {symbol}")
    df_nse.index = pd.to_datetime(df_nse.index)
    return df_nse.sort_index()
