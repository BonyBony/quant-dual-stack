import json
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

import pandas as pd
import pytest


def _make_bhavcopy_zip(symbol: str, timestamp: str) -> bytes:
    headers = (
        "SYMBOL,SERIES,OPEN,HIGH,LOW,CLOSE,LAST,PREVCLOSE,TOTTRDQTY,TOTTRDVAL," \
        "TIMESTAMP,TOTALTRADES,ISIN,Unnamed: 13\n"
    )
    row = f"{symbol},EQ,100,110,90,105,105,99,123456,1000000,{timestamp},10,ISIN123,\n"
    buf = BytesIO()
    with ZipFile(buf, "w") as zf:
        zf.writestr("cmTEST.csv", headers + row)
    buf.seek(0)
    return buf.getvalue()


def test_load_daily_falls_back_to_nse(monkeypatch):
    from common.data import yf_loader

    symbol = "ZOMATO.NS"
    start = end = "2024-01-02"

    def fake_download(*_, **__):
        raise yf_loader.YFTzMissingError("no tz")

    zip_bytes = _make_bhavcopy_zip("ZOMATO", "02-JAN-2024")

    class FakeResponse:
        def __init__(self, status_code: int, content: bytes):
            self.status_code = status_code
            self.content = content

    def fake_get(url, *_, **__):
        if "archives.nseindia.com" in url:
            return FakeResponse(200, zip_bytes)
        return FakeResponse(404, b"")

    monkeypatch.setattr(yf_loader.yf, "download", fake_download)
    monkeypatch.setattr(yf_loader.requests, "get", fake_get)

    df = yf_loader.load_daily(symbol, start, end)

    assert not df.empty
    assert list(df.columns) == ["open", "high", "low", "close", "volume"]
    assert pd.Timestamp("2024-01-02") in df.index


def test_build_macd_signals_writes_csv(tmp_path: Path, monkeypatch):
    from execution.jobs import build_macd_signals as job

    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    params_file = cache_dir / "macd_params_2024-01-02.json"
    params_file.write_text(json.dumps({"fast": 12, "slow": 26, "signal": 9}))

    signal_dir = tmp_path / "signals"

    monkeypatch.setenv("CPO_OUT_DIR", str(cache_dir))
    monkeypatch.setenv("SIGNALS_DATA_DIR", str(signal_dir))
    monkeypatch.setenv("CPO_SYMBOL", "HDFCBANK.NS")

    dates = pd.to_datetime(["2024-01-01", "2024-01-02"])
    prices = pd.Series([100, 105], index=dates, name="close")
    df_prices = pd.DataFrame({
        "open": [99, 102],
        "high": [101, 107],
        "low": [98, 101],
        "close": [100, 105],
        "volume": [1e6, 1.1e6],
    }, index=dates)

    monkeypatch.setattr(job, "load_daily", lambda *_, **__: df_prices)
    monkeypatch.setattr(job, "DATE", None, raising=False)

    job.main()

    files = list(signal_dir.glob("signals_*.csv"))
    assert len(files) == 1
    df_signal = pd.read_csv(files[0])
    expected_cols = {
        "ts",
        "symbol",
        "position",
        "entry",
        "exit",
        "flip",
        "risk_fraction",
        "macd_fast",
        "macd_slow",
        "macd_signal",
    }
    assert expected_cols.issubset(df_signal.columns)
    assert (df_signal["symbol"] == "HDFCBANK.NS").all()
