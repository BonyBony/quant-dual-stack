import argparse, json, joblib, pathlib, yaml, pandas as pd
from dataclasses import dataclass
from common.data.yf_loader import load_daily
from common.features.chan_ex7_1_daily import compute_features_daily
from research.labels.next_day_strategy_return import build_macd_labels
from research.models.regressors import get_regressor
from research.optimization.conditional_opt import ConditionalParamOptimizer
from strategies.macd import MACDParams
from evaluation.sharpe import sharpe_ratio

@dataclass
class MACDCPOConfig:
    symbol: str
    train_start: str
    train_end: str
    test_start: str
    test_end: str
    macd_grid: dict
    lookbacks: list
    model: dict
    objective_freq_per_year: int = 252
    artifacts_dir: str = "research/artifacts/macd_cpo"

def main(cfg_path: str):
    cfg = MACDCPOConfig(**yaml.safe_load(open(cfg_path)))
    art = pathlib.Path(cfg.artifacts_dir); art.mkdir(parents=True, exist_ok=True)

    df = load_daily(cfg.symbol, cfg.train_start, cfg.test_end)
    pg = [MACDParams(f,s,sig) for f in cfg.macd_grid['fast']
                          for s in cfg.macd_grid['slow'] if f < s
                          for sig in cfg.macd_grid['signal']]
    param_grid_dicts = [p.__dict__ for p in pg]

    days = pd.to_datetime(df.index.normalize().unique())
    train_days = days[(days >= pd.Timestamp(cfg.train_start)) & (days <= pd.Timestamp(cfg.train_end))]
    test_days  = days[(days >= pd.Timestamp(cfg.test_start))  & (days <= pd.Timestamp(cfg.test_end))]

    labels_df = build_macd_labels(df, list(train_days)+[test_days[0]], pg)

    X_rows = []
    for d in train_days:
        feats = compute_features_daily(df.loc[:d], cfg.lookbacks)
        for p in pg:
            X_rows.append(pd.concat([feats, pd.Series(p.__dict__)]))
    X = pd.DataFrame(X_rows)
    y = labels_df['label'].values

    model = get_regressor(cfg.model['name'])
    cpo = ConditionalParamOptimizer(model, param_grid_dicts).fit(X, y)

    # Save artifacts
    joblib.dump(model, art/"model.pkl")
    json.dump(param_grid_dicts, open(art/"param_grid.json","w"))
    json.dump({"lookbacks": cfg.lookbacks,
               "symbol": cfg.symbol,
               "data_start": cfg.train_start,
               "feature_cols": list(X.columns)},
              open(art/"feature_meta.json","w"))

    # Quick OOS check
    pnl_oos = []
    from strategies.macd import MACDStrategy
    strat = MACDStrategy()
    for i in range(len(test_days)-1):
        d = test_days[i]; d_next = test_days[i+1]
        feats_today = compute_features_daily(df.loc[:d], cfg.lookbacks)
        best = cpo.predict_params(feats_today)
        pnl = strat.run_day(df.loc[(df.index>=d_next)&(df.index<d_next+pd.Timedelta(days=1))],
                            MACDParams(**best))
        pnl_oos.append(pnl)
    sharpe = sharpe_ratio(pd.Series(pnl_oos), cfg.objective_freq_per_year)
    print("OOS Sharpe (quick check):", sharpe)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/cpo/macd_cpo.yaml")
    args = parser.parse_args()
    main(args.config)
