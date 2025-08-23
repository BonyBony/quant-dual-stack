# research/cpo/engine.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Tuple
import numpy as np
import pandas as pd

from common.data.yf_loader import load_daily
from common.features.chan_ex7_1_daily import compute_features_daily
from common.validation.purged_cv import PurgedGroupTimeSeriesSplit

from research.strategies.macd import MACDParams, MACDStrategy
from research.backtesting.walk_forward import CostModel  # reuse your linear cost model

# ---------------------------- helpers ----------------------------

def build_param_grid(macd_grid: Dict) -> Tuple[List[MACDParams], List[Dict]]:
    fast = macd_grid["fast"]; slow = macd_grid["slow"]; signal = macd_grid["signal"]
    pg = [MACDParams(f, s, sg) for f in fast for s in slow if f < s for sg in signal]
    return pg, [p.__dict__ for p in pg]

def _next_day_net_pnl(close: pd.Series, day_i: int, p: MACDParams, cost_model: CostModel) -> float:
    """
    Label = net PnL for day_{i+1} using position from day_i and turnover cost on change at day_{i+1}.
    close is a 1D Series aligned to trading days.
    """
    if day_i < 1 or day_i + 1 >= len(close):
        return np.nan

    # history up to day_i
    hist_i   = pd.DataFrame({"close": close.iloc[: day_i+1]})
    hist_ip1 = pd.DataFrame({"close": close.iloc[: day_i+2]})

    strat = MACDStrategy()
    pos_i   = strat.position(hist_i,   p)
    pos_ip1 = strat.position(hist_ip1, p)

    ret_ip1 = (close.iloc[day_i+1] - close.iloc[day_i]) / close.iloc[day_i]
    turnover = abs(pos_ip1 - pos_i) * 1.0  # unit notional fraction
    cost = cost_model.turnover_cost(turnover)
    return float(pos_i * ret_ip1 - cost)

# ----------------------- training table --------------------------

def build_training_table(
    df: pd.DataFrame,
    train_days: pd.DatetimeIndex,
    param_grid: List[MACDParams],
    lookbacks: List[int],
    cost_model: CostModel,
) -> Tuple[pd.DataFrame, np.ndarray, np.ndarray, int]:
    """
    Returns:
      X: DataFrame of features + params
      y: 1D np.array of net next-day PnL
      groups: np.array of dates (same length as rows in X)
      max_slow: int (for later slices)
    """
    max_slow = max(p.slow for p in param_grid)
    close = df["close"].astype(float).copy()
    # To avoid early-bar cold-start, start after max_slow
    day_list = [d for d in train_days if d in close.index]
    # Build labels first (one per (date, param))
    rows_X = []
    y_vals = []
    g_vals = []

    for d in day_list:
        # index of d in close
        i = close.index.get_loc(d)
        if isinstance(i, slice):  # shouldn't happen with unique index
            i = i.start
        if i < max_slow or i+1 >= len(close):
            continue

        # features as of day d (use data up to d)
        feats = compute_features_daily(df.loc[:d], lookbacks)

        for p in param_grid:
            # net next-day pnl label
            lbl = _next_day_net_pnl(close, i, p, cost_model)
            if np.isnan(lbl):
                continue
            # row = features + param columns
            rows_X.append(pd.concat([feats, pd.Series(p.__dict__)]))
            y_vals.append(lbl)
            g_vals.append(d)  # group = date

    X = pd.DataFrame(rows_X).reset_index(drop=True)
    y = np.asarray(y_vals, dtype=float)
    groups = np.asarray(g_vals)
    return X, y, groups, max_slow

# -------------------------- model fit ----------------------------

from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_squared_error

@dataclass
class CPOCVReport:
    splits: int
    embargo_groups: int
    rmse_mean: float
    rmse_std: float
    fold_rmses: List[float]

def fit_cpo_model(
    X: pd.DataFrame,
    y: np.ndarray,
    groups: np.ndarray,
    n_splits: int = 5,
    embargo_groups: int = 1,
    model_name: str = "hgbt",
):
    splitter = PurgedGroupTimeSeriesSplit(n_splits=n_splits, embargo_groups=embargo_groups)

    # Choose model
    if model_name.lower() in ("hgbt", "histgbrt", "histgradientboosting"):
        model = HistGradientBoostingRegressor(
            learning_rate=0.05,
            max_depth=None,
            max_iter=400,
            l2_regularization=0.0,
            random_state=42,
        )
    else:
        # fallback to GBRT
        from sklearn.ensemble import GradientBoostingRegressor
        model = GradientBoostingRegressor(random_state=42)

    # CV diagnostics (optional)
    rmses = []
    for tr_idx, va_idx in splitter.split(X, y, groups):
        if len(np.unique(groups[tr_idx])) == 0 or len(np.unique(groups[va_idx])) == 0:
            continue
        model.fit(X.iloc[tr_idx], y[tr_idx])
        yp = model.predict(X.iloc[va_idx])
        rmses.append(mean_squared_error(y[va_idx], yp, squared=False))

    report = CPOCVReport(
        splits=n_splits,
        embargo_groups=embargo_groups,
        rmse_mean=float(np.mean(rmses)) if rmses else float("nan"),
        rmse_std=float(np.std(rmses)) if rmses else float("nan"),
        fold_rmses=[float(x) for x in rmses],
    )

    # Final fit on ALL training data (time-ordered, no shuffling)
    model.fit(X, y)
    return model, report

# ----------------------- selection utilities ---------------------

def predict_grid(model, feats_today: pd.Series, param_grid_dicts: List[Dict]) -> pd.Series:
    rows = [pd.concat([feats_today, pd.Series(p)]) for p in param_grid_dicts]
    XF = pd.DataFrame(rows)
    preds = model.predict(XF)
    out = pd.Series(preds, index=[tuple(sorted(p.items())) for p in param_grid_dicts], name="pred")
    return out

def select_params_for_day(model, feats_today: pd.Series, param_grid_dicts: List[Dict]) -> Dict:
    preds = predict_grid(model, feats_today, param_grid_dicts)
    # index is tuple of sorted (k,v) pairs; recover dict
    best_key = preds.idxmax()
    return dict(best_key)
