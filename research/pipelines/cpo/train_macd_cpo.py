"""
Train Conditional-Parameter-Optimization model for daily-bar MACD strategy
-------------------------------------------------------------------------

‣ Builds non-zero labels using a rolling window of (max_slow + 2) bars  
‣ Aligns X (features) and y (labels) so lengths match  
‣ Saves model + metadata + quick OOS Sharpe
"""

import argparse, json, joblib, pathlib, yaml, pandas as pd
from dataclasses import dataclass
from common.data.yf_loader import load_daily
from common.features.chan_ex7_1_daily import compute_features_daily
from research.models.regressors import get_regressor
from research.optimization.conditional_opt import ConditionalParamOptimizer
from research.strategies.macd import MACDParams, MACDStrategy
from research.evaluation.sharpe import sharpe_ratio

# --------------------------------------------------------------------- #
# Config dataclass
# --------------------------------------------------------------------- #
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


# --------------------------------------------------------------------- #
# Helper: build labels with enough history for MACD
# --------------------------------------------------------------------- #
def build_macd_labels(
    df: pd.DataFrame,
    days: list[pd.Timestamp],
    param_grid: list[MACDParams],
) -> pd.DataFrame:
    strat = MACDStrategy()
    rows = []
    max_slow = max(p.slow for p in param_grid)
    for i in range(max_slow, len(days) - 1):
        d = days[i]
        d_next = days[i + 1]
        if {d, d_next}.issubset(df.index):
            df_slice = df.loc[df.index <= d_next].tail(max_slow + 2)
            for p in param_grid:
                pnl = strat.run_day(df_slice, p)
                rows.append({"date": d, **p.__dict__, "label": pnl})
    return pd.DataFrame(rows)


# --------------------------------------------------------------------- #
# Main training routine
# --------------------------------------------------------------------- #
def main(cfg_path: str):
    cfg = MACDCPOConfig(**yaml.safe_load(open(cfg_path)))
    art_dir = pathlib.Path(cfg.artifacts_dir)
    art_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------ #
    # Load data
    # ------------------------------------------------------------------ #
    df = load_daily(cfg.symbol, cfg.train_start, cfg.test_end)

    # Build MACD parameter grid
    pg = [
        MACDParams(f, s, sig)
        for f in cfg.macd_grid["fast"]
        for s in cfg.macd_grid["slow"]
        if f < s
        for sig in cfg.macd_grid["signal"]
    ]
    param_grid_dicts = [p.__dict__ for p in pg]

    days = pd.to_datetime(df.index.normalize().unique())
    train_days = days[
        (days >= pd.Timestamp(cfg.train_start)) & (days <= pd.Timestamp(cfg.train_end))
    ]
    test_days = days[
        (days >= pd.Timestamp(cfg.test_start)) & (days <= pd.Timestamp(cfg.test_end))
    ]

    # ------------------------------------------------------------------ #
    # Labels (y)
    # ------------------------------------------------------------------ #
    labels_df = build_macd_labels(df, list(train_days) + [test_days[0]], pg)
    y = labels_df["label"].values
    print("\n--- LABELS DF SUMMARY ---")
    print(labels_df["label"].describe())

    # ------------------------------------------------------------------ #
    # Features (X) – align with LABEL dates
    # ------------------------------------------------------------------ #
    label_dates = labels_df["date"].unique()           # ⬅️ use same dates
    X_rows = []
    for d in label_dates:                              # ⬅️ iterate label days
        feats = compute_features_daily(df.loc[:d], cfg.lookbacks)
        for p in pg:
            X_rows.append(pd.concat([feats, pd.Series(p.__dict__)]))
    X = pd.DataFrame(X_rows).reset_index(drop=True)

    assert len(X) == len(y), f"X rows {len(X)} != y rows {len(y)} – lengths must match"

    # ------------------------------------------------------------------ #
    # Train model + CPO engine
    # ------------------------------------------------------------------ #
    model = get_regressor(cfg.model["name"])
    cpo = ConditionalParamOptimizer(model, param_grid_dicts).fit(X, y)

    # ------------------------------------------------------------------ #
    # Save artifacts
    # ------------------------------------------------------------------ #
    joblib.dump(model, art_dir / "model.pkl")
    json.dump(param_grid_dicts, open(art_dir / "param_grid.json", "w"))
    json.dump(
        {
            "lookbacks": cfg.lookbacks,
            "symbol": cfg.symbol,
            "data_start": cfg.train_start,
            "feature_cols": list(X.columns),
        },
        open(art_dir / "feature_meta.json", "w"),
    )

    # ------------------------------------------------------------------ #
    # Quick OOS check
    # ------------------------------------------------------------------ #
    max_slow = max(p.slow for p in pg)          #  ←  add this line back

    strat = MACDStrategy()
    pnl_oos = []
    for i in range(max_slow, len(test_days) - 1):
        d, d_next = test_days[i], test_days[i + 1]
        slice_oos = df.loc[df.index <= d_next].tail(max_slow + 2)
        feats_today = compute_features_daily(df.loc[:d], cfg.lookbacks)
        best = cpo.predict_params(feats_today)
        pnl_oos.append(strat.run_day(slice_oos, MACDParams(**best)))

    sharpe = sharpe_ratio(pd.Series(pnl_oos), cfg.objective_freq_per_year)
    print("OOS Sharpe (quick check):", sharpe)


# --------------------------------------------------------------------- #
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="research/configs/cpo/macd_cpo.yaml")
    main(parser.parse_args().config)
