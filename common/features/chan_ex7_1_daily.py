import pandas as pd
import numpy as np
import ta
from typing import Sequence

DEFAULT_LOOKBACKS = [5, 10, 20, 40, 80, 160, 320]

def compute_features_daily(df: pd.DataFrame, lookbacks: Sequence[int]) -> pd.Series:
    o, h, l, c, v = (df['open'], df['high'], df['low'], df['close'], df['volume'])
    feat = {}
    # Precompute AO once (it's always 5/34)
    try:
        if len(h) >= 34 and len(l) >= 34:
            ao_full = ta.momentum.AwesomeOscillatorIndicator(h, l, window1=5, window2=34).awesome_oscillator()
        else:
            ao_full = pd.Series([0]*len(df), index=df.index)
    except Exception as e:
        ao_full = pd.Series([0]*len(df), index=df.index)
    for L in lookbacks:
        # Bollinger Bands Z-score
        try:
            if len(c) >= L:
                ema = c.ewm(span=L).mean()
                var = (c - ema).pow(2).ewm(span=L).mean()
                z = (c.iloc[-1] - ema.iloc[-1]) / np.sqrt(var.iloc[-1]) if var.iloc[-1] > 0 else 0
            else:
                z = 0
        except Exception as e:
            z = 0
        feat[f"boll_z_{L}"] = z

        # Money Flow Index
        try:
            if len(c) >= L:
                mfi = ta.volume.MFIIndicator(h, l, c, v, window=L).money_flow_index().iloc[-1]
            else:
                mfi = 0
        except Exception as e:
            mfi = 0
        feat[f"mfi_{L}"] = mfi

        # Force Index
        try:
            if len(c) >= L:
                fi = ta.volume.ForceIndexIndicator(c, v, window=L).force_index().iloc[-1]
            else:
                fi = 0
        except Exception as e:
            fi = 0
        feat[f"force_{L}"] = fi

        # Donchian Channel
        try:
            if len(h) >= L and len(l) >= L:
                dc_high = h.rolling(L).max().iloc[-1]
                dc_low  = l.rolling(L).min().iloc[-1]
                donch = (dc_high - dc_low) / c.iloc[-1] if c.iloc[-1] != 0 else 0
            else:
                donch = 0
        except Exception as e:
            donch = 0
        feat[f"donch_w_{L}"] = donch

        # ATR
        try:
            if len(c) >= L:
                atr = ta.volatility.AverageTrueRange(h, l, c, window=L).average_true_range().iloc[-1]
            else:
                atr = 0
        except Exception as e:
            atr = 0
        feat[f"atr_{L}"] = atr

        # AO (Awesome Oscillator)
        try:
            ao = ao_full.iloc[-1] if len(ao_full) > 0 else 0
        except Exception as e:
            ao = 0
        feat[f"ao_{L}"] = ao

        # ADX
        try:
            if len(c) >= L:
                adx = ta.trend.ADXIndicator(h, l, c, window=L).adx().iloc[-1]
            else:
                adx = 0
        except Exception as e:
            adx = 0
        feat[f"adx_{L}"] = adx

    return pd.Series(feat)
