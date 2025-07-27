import pandas as pd
import numpy as np
import ta
from typing import Sequence

DEFAULT_LOOKBACKS = [5, 10, 20, 40, 80, 160, 320]

def compute_features_daily(df: pd.DataFrame, lookbacks: Sequence[int]) -> pd.Series:
    o, h, l, c, v = (df['open'], df['high'], df['low'], df['close'], df['volume'])
    feat = {}
    ao_full = ta.momentum.AwesomeOscillatorIndicator(h, l, window1=5, window2=34).awesome_oscillator()
    for L in lookbacks:
        ema = c.ewm(span=L).mean()
        var = (c - ema).pow(2).ewm(span=L).mean()
        z = (c.iloc[-1] - ema.iloc[-1]) / np.sqrt(var.iloc[-1]) if var.iloc[-1] > 0 else 0
        feat[f"boll_z_{L}"] = z

        mfi = ta.volume.MFIIndicator(h, l, c, v, window=L).money_flow_index().iloc[-1]
        feat[f"mfi_{L}"] = mfi

        fi = ta.volume.ForceIndexIndicator(c, v, window=L).force_index().iloc[-1]
        feat[f"force_{L}"] = fi

        dc_high = h.rolling(L).max().iloc[-1]
        dc_low  = l.rolling(L).min().iloc[-1]
        feat[f"donch_w_{L}"] = (dc_high - dc_low) / c.iloc[-1] if c.iloc[-1] != 0 else 0

        atr = ta.volatility.AverageTrueRange(h, l, c, window=L).average_true_range().iloc[-1]
        feat[f"atr_{L}"] = atr

        feat[f"ao_{L}"] = ao_full.iloc[-1]

        adx = ta.trend.ADXIndicator(h, l, c, window=L).adx().iloc[-1]
        feat[f"adx_{L}"] = adx

    return pd.Series(feat)
