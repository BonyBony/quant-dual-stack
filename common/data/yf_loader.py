# common/data/yf_loader.py
from __future__ import annotations

import pandas as pd
import yfinance as yf

try:  # yfinance exposes the error in newer releases
    from yfinance.shared._exceptions import YFTzMissingError
except Exception:  # pragma: no cover - older yfinance versions
    YFTzMissingError = Exception  # type: ignore

try:
    from nsepy import get_history
except ImportError:  # pragma: no cover - optional dependency
    get_history = None  # type: ignore

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
        if get_history is None:
            raise RuntimeError("nsepy not available for NSE fallback")
        sym = symbol.replace(".NS", "").upper()
        start_dt = pd.Timestamp(start).date()
        end_dt = pd.Timestamp(end).date()
        df = get_history(symbol=sym, start=start_dt, end=end_dt)
        if df.empty:
            return df
        df = df.rename(
            columns={
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume",
            }
        )
        cols = [c for c in ["open", "high", "low", "close", "volume"] if c in df.columns]
        return df[cols].dropna(how="all").copy()

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
