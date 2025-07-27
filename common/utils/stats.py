import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller

def engle_granger(log_y, log_x, maxlag=5):
    X = sm.add_constant(log_x)
    res = sm.OLS(log_y, X).fit()
    resid = res.resid
    pval = adfuller(resid, maxlag=maxlag, regression='c')[1]
    beta = res.params[1]
    return beta, resid, pval

def half_life_ou(resid):
    e = resid.dropna()
    de = e.diff().dropna()
    e_lag = e.shift(1).dropna()
    X = sm.add_constant(e_lag.loc[de.index])
    try:
        b = sm.OLS(de, X).fit().params[1]
    except Exception:
        return np.nan
    return -np.log(2)/b if b < 0 else np.inf
