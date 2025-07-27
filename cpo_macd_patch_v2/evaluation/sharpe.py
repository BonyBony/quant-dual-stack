import numpy as np

def sharpe_ratio(rets, freq_per_year=252):
    rets = np.asarray(rets)
    if rets.std(ddof=1) == 0:
        return 0.0
    return np.sqrt(freq_per_year) * rets.mean() / rets.std(ddof=1)
