import pandas as pd
from dataclasses import dataclass
from typing import List
from data.loaders.yf_loader import load_daily
from data.features.chan_ex7_1_daily import compute_features_daily
from labels.next_day_strategy_return import build_macd_labels
from models.regressors import get_regressor
from optimization.conditional_opt import ConditionalParamOptimizer
from strategies.macd import MACDParams, MACDStrategy
from evaluation.sharpe import sharpe_ratio

@dataclass
class MACDCPOConfig:
    symbol: str
    train_start: str
    train_end: str
    test_start: str
    test_end: str
    macd_grid: dict
    lookbacks: List[int]
    model: dict
    objective_freq_per_year: int = 252

def run_macd_cpo(cfg: MACDCPOConfig):
    df = load_daily(cfg.symbol, cfg.train_start, cfg.test_end)
    pg = []
    for f in cfg.macd_grid['fast']:
        for s in cfg.macd_grid['slow']:
            if f >= s:
                continue
            for sig in cfg.macd_grid['signal']:
                pg.append(MACDParams(f, s, sig))
    param_grid_dicts = [p.__dict__ for p in pg]

    days = pd.to_datetime(df.index.normalize().unique())
    train_days = days[(days >= pd.Timestamp(cfg.train_start)) & (days <= pd.Timestamp(cfg.train_end))]
    test_days  = days[(days >= pd.Timestamp(cfg.test_start))  & (days <= pd.Timestamp(cfg.test_end))]

    labels_df = build_macd_labels(df, list(train_days) + [test_days[0]], pg)

    X_rows = []
    for day in train_days:
        feats = compute_features_daily(df.loc[:day], cfg.lookbacks)
        for p in pg:
            X_rows.append(pd.concat([feats, pd.Series(p.__dict__)]))
    X = pd.DataFrame(X_rows).reset_index(drop=True)
    y = labels_df['label'].values

    model = get_regressor(cfg.model['name'])
    cpo = ConditionalParamOptimizer(model, param_grid_dicts)
    cpo.fit(X, y)

    strat = MACDStrategy()
    pnl_oos = []
    idx_oos = []
    for i in range(len(test_days) - 1):
        d = test_days[i]
        d_next = test_days[i + 1]
        feats_today = compute_features_daily(df.loc[:d], cfg.lookbacks)
        best = cpo.predict_params(feats_today)
        pnl = strat.run_day(df.loc[(df.index >= d_next) & (df.index < d_next + pd.Timedelta(days=1))],
                            MACDParams(**best))
        pnl_oos.append(pnl)
        idx_oos.append(d_next)

    pnl_series = pd.Series(pnl_oos, index=idx_oos)
    sharpe = sharpe_ratio(pnl_series, cfg.objective_freq_per_year)
    return sharpe, pnl_series, cpo
