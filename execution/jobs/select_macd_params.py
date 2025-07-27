import os, json, joblib, pandas as pd
from datetime import date
from common.data.yf_loader import load_daily
from common.features.chan_ex7_1_daily import compute_features_daily
from execution.param_selector.conditional_param_runtime import ConditionalParamRuntime

ART_DIR = os.getenv("CPO_MACD_ART_DIR", "research/artifacts/macd_cpo")
OUT_DIR = os.getenv("CPO_OUT_DIR", "execution/cache")
SYMBOL  = os.getenv("CPO_SYMBOL", "ZOMATO.NS")

meta = json.load(open(f"{ART_DIR}/feature_meta.json"))
model = joblib.load(f"{ART_DIR}/model.pkl")
param_grid = json.load(open(f"{ART_DIR}/param_grid.json"))

df = load_daily(SYMBOL, meta["data_start"], date.today().isoformat())
feats = compute_features_daily(df, meta["lookbacks"])
runtime = ConditionalParamRuntime(model, param_grid, meta["feature_cols"])
best = runtime.pick(feats)

os.makedirs(OUT_DIR, exist_ok=True)
out_path = f"{OUT_DIR}/macd_params_{date.today()}.json"
with open(out_path, "w") as f:
    json.dump(best, f)
print("Saved:", out_path)
