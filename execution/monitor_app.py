import streamlit as st
import pandas as pd
import time
import pathlib

st.set_page_config(page_title="Backtrader Live PnL", layout="wide")
st.title("Backtrader Live PnL")

placeholder = st.empty()

DATA_DIR = pathlib.Path("data")
PNL_FILE  = DATA_DIR / "pnl.csv"

def load_pnl():
    if not PNL_FILE.exists():
        return pd.DataFrame(columns=["ts", "eq"])
    return pd.read_csv(PNL_FILE, names=["ts", "eq"])

while True:
    df = load_pnl()
    if not df.empty:
        df["ts"] = pd.to_datetime(df["ts"])
        placeholder.line_chart(df.set_index("ts")["eq"])
    time.sleep(5)
