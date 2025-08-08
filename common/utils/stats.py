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

def calc_cagr(returns: pd.Series, per_year=252):
    total = (1 + returns).prod()
    years = len(returns) / per_year
    return total**(1 / years) - 1 if years > 0 else np.nan

def calc_sharpe(returns: pd.Series, risk_free=0.0, per_year=252):
    excess = returns - (risk_free / per_year)
    return np.sqrt(per_year) * excess.mean() / excess.std()

def calc_max_drawdown(returns: pd.Series):
    cum = (1 + returns).cumprod()
    return (cum / cum.cummax() - 1).min()

def get_return_metrics(returns: pd.Series, name="Strategy"):
    return {
        "name": name,
        "sharpe": calc_sharpe(returns),
        "cagr": calc_cagr(returns),
        "max_drawdown": calc_max_drawdown(returns),
        "mean_return": returns.mean(),
        "vol": returns.std(),
        "win_rate": (returns > 0).mean()
    }