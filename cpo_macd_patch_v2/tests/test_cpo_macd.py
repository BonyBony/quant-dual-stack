import pandas as pd
from pipelines.macd_cpo_pipeline import run_macd_cpo, MACDCPOConfig

def test_macd_pipeline_smoke():
    cfg = MACDCPOConfig(
        symbol="ZOMATO.NS",
        train_start="2023-01-01",
        train_end="2023-12-31",
        test_start="2024-01-01",
        test_end="2024-12-31",
        macd_grid={"fast":[6,8], "slow":[20,26], "signal":[5]},
        lookbacks=[5,10],
        model={"name":"gbrt"}
    )
    sharpe, pnl, _ = run_macd_cpo(cfg)
    assert isinstance(sharpe, float)
    assert isinstance(pnl, pd.Series)
