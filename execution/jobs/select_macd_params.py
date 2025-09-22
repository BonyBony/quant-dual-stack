import os, json, joblib, pandas as pd
from datetime import date
from common.data.yf_loader import load_daily
from common.features.chan_ex7_1_daily import compute_features_daily

try:
    from execution.param_selector.conditional_param_runtime import ConditionalParamRuntime
except ImportError:  # fallback when /app already equals execution dir
    from param_selector.conditional_param_runtime import ConditionalParamRuntime

ART_DIR = os.getenv("CPO_MACD_ART_DIR", "research/artifacts/macd_cpo")
if not os.path.isdir(ART_DIR):
    alt = "/app/artifacts/macd_cpo"
    if os.path.isdir(alt):
        ART_DIR = alt
OUT_DIR = os.getenv("CPO_OUT_DIR", "execution/cache")
SYMBOL  = os.getenv("CPO_SYMBOL", "ZOMATO.NS")

meta = json.load(open(f"{ART_DIR}/feature_meta.json"))
model = joblib.load(f"{ART_DIR}/model.pkl")
param_grid = json.load(open(f"{ART_DIR}/param_grid.json"))

df = load_daily(SYMBOL, meta["data_start"], date.today().isoformat())
feats = compute_features_daily(df, meta["lookbacks"])
runtime = ConditionalParamRuntime(model, param_grid, meta["feature_cols"])
best = runtime.pick(feats)

if not os.path.isabs(OUT_DIR):
    base = os.getcwd()
    OUT_DIR = os.path.abspath(os.path.join(base, OUT_DIR))
    if base.rstrip("/") == "/app" and not os.path.exists(os.path.dirname(OUT_DIR)):
        OUT_DIR = os.path.join(base, "cache")
os.makedirs(OUT_DIR, exist_ok=True)
out_path = os.path.join(OUT_DIR, f"macd_params_{date.today()}.json")
with open(out_path, "w") as f:
    json.dump(best, f)
print("Saved:", out_path)
