import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller

__all__ = ["engle_granger", "half_life_ou", "get_return_metrics"]

def engle_granger(log_y, log_x, maxlag=5):
    X = sm.add_constant(log_x)
    res = sm.OLS(log_y, X).fit()
    resid = res.resid
    pval = adfuller(resid, maxlag=maxlag, regression='c')[1]
    beta = res.params[1]
    return beta, resid, pval

def half_life_ou(resid):
    e = pd.Series(resid).dropna()
    if len(e) < 3:
        return np.nan
    de = e.diff().dropna()
    e_lag = e.shift(1).dropna()
    X = sm.add_constant(e_lag.loc[de.index])
    try:
        b = sm.OLS(de, X).fit().params[1]
    except Exception:
        return np.nan
    return -np.log(2)/b if b < 0 else np.inf

def get_return_metrics(rets: pd.Series, ann_freq: int = 252) -> dict:
    r = pd.Series(rets).dropna()
    if r.empty:
        return {"n":0,"mean":0.0,"std":0.0,"sharpe":0.0,"cagr":0.0,"max_dd":0.0,"win_rate":0.0}
    mu, sd = r.mean(), r.std()
    sharpe = (np.sqrt(ann_freq)*mu/sd) if sd != 0 else 0.0
    cum = (1.0 + r).prod()
    years = len(r)/ann_freq
    cagr = (cum**(1/years) - 1.0) if years>0 else 0.0
    eq = (1.0 + r).cumprod()
    max_dd = (eq/eq.cummax() - 1.0).min() if not eq.empty else 0.0
    win_rate = float((r>0).sum())/len(r)
    return {"n":int(len(r)),"mean":float(mu),"std":float(sd),
            "sharpe":float(sharpe),"cagr":float(cagr),
            "max_dd":float(max_dd),"win_rate":float(win_rate)}
