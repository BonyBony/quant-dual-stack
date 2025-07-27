import pandas as pd
from dataclasses import dataclass
from typing import List
from data.loaders.yf_loader import load_pair_daily
from strategies.spread_pair import SpreadPairStrategy, SpreadParams
from data.features.chan_ex7_1_daily import compute_features_daily
from models.regressors import get_regressor
from optimization.conditional_opt import ConditionalParamOptimizer
from evaluation.sharpe import sharpe_ratio

@dataclass
class SpreadCPOConfig:
    primary: str
    hedge: str
    train_start: str
    train_end: str
    test_start: str
    test_end: str
    entry_threshold: List[float]
    lookback: List[int]
    beta_mode: List[str]
    lookbacks_feat: List[int]
    model: dict
    objective_freq_per_year: int = 252

def run_spread_cpo(cfg: SpreadCPOConfig):
    df_close = load_pair_daily(cfg.primary, cfg.hedge, cfg.train_start, cfg.test_end)
    strat = SpreadPairStrategy(cfg.primary, cfg.hedge)

    pg = []
    for et in cfg.entry_threshold:
        for lb in cfg.lookback:
            for bm in cfg.beta_mode:
                pg.append(SpreadParams(et, lb, bm))
    param_grid_dicts = [p.__dict__ for p in pg]

    days = pd.to_datetime(df_close.index.normalize().unique())
    train_days = days[(days >= pd.Timestamp(cfg.train_start)) & (days <= pd.Timestamp(cfg.train_end))]
    test_days  = days[(days >= pd.Timestamp(cfg.test_start))  & (days <= pd.Timestamp(cfg.test_end))]

    pnl_full = {}
    for p in pg:
        pnl_series = strat.run_series(df_close.loc[train_days.min():test_days.max()], p)
        pnl_full[p] = pnl_series

    rows_X, rows_y = [], []
    for i in range(len(train_days) - 1):
        d = train_days[i]
        base = df_close[[cfg.primary]].rename(columns={cfg.primary: 'close'}).assign(
            open=lambda x: x['close'], high=lambda x: x['close'], low=lambda x: x['close'], volume=0
        )
        feat = compute_features_daily(base.loc[:d], cfg.lookbacks_feat)
        for p in pg:
            rows_X.append(pd.concat([feat, pd.Series(p.__dict__)]))
            rows_y.append(pnl_full[p].loc[train_days[i+1]])
    X = pd.DataFrame(rows_X)
    y = pd.Series(rows_y)

    model = get_regressor(cfg.model['name'])
    cpo = ConditionalParamOptimizer(model, param_grid_dicts)
    cpo.fit(X, y)

    pnl_oos = []
    idx = []
    for i in range(len(test_days) - 1):
        d = test_days[i]
        d_next = test_days[i+1]
        base = df_close[[cfg.primary]].rename(columns={cfg.primary: 'close'}).assign(
            open=lambda x: x['close'], high=lambda x: x['close'], low=lambda x: x['close'], volume=0
        )
        feat = compute_features_daily(base.loc[:d], cfg.lookbacks_feat)
        best = cpo.predict_params(feat)
        pnl_series = strat.run_series(df_close.loc[d_next:d_next], SpreadParams(**best))
        pnl = pnl_series.iloc[-1]
        pnl_oos.append(pnl)
        idx.append(d_next)

    pnl_series = pd.Series(pnl_oos, index=idx)
    sharpe = sharpe_ratio(pnl_series, cfg.objective_freq_per_year)
    return sharpe, pnl_series, cpo
