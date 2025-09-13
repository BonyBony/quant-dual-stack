# research/analysis/run_cost_stop_sweep.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Dict, Tuple, List
import numpy as np
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed
import os

from common.data.yf_loader import load_daily
from common.utils.stats import get_return_metrics
from research.strategies.macd import MACDParams, precompute_macd_positions
from research.backtesting.walk_forward import (
    WalkForwardBacktester, PositionSizer, StopLoss, CostModel
)

@dataclass
class SweepConfig:
    symbol: str
    macd_grid: Dict[str, List[int]]
    start: str = "2019-01-01"
    train_years: int = 3
    test_months: int = 6
    commission_bps_list: Iterable[int] = (0, 5, 10)
    slippage_bps_list:   Iterable[int] = (0, 5, 10)
    stop_list:           Iterable[float] = (0.01, 0.015, 0.02, 0.03)
    n_jobs: int = max(os.cpu_count() - 1, 1) if os.cpu_count() else 1  # parallel workers

def _build_param_grid(grid: Dict[str, List[int]]) -> List[MACDParams]:
    fasts, slows, sigs = grid["fast"], grid["slow"], grid["signal"]
    return [MACDParams(f, s, sg) for f in fasts for s in slows if f < s for sg in sigs]

def _eval_combo(df: pd.DataFrame,
                params: List[MACDParams],
                pos_cache: Dict[Tuple[int,int,int], np.ndarray],
                cbps: int, sbps: int, stop: float,
                train_window: int, test_window: int) -> Dict:
    wf = WalkForwardBacktester(
        strategy=None,  # not used because we rely on cached positions
        position_sizer=PositionSizer(risk_per_trade=1.0),
        stop_loss=StopLoss(pct=float(stop)),
        cost_model=CostModel(commission_pct=cbps/10000.0, slippage_pct=sbps/10000.0),
        train_window=train_window,
        test_window=test_window,
        initial_equity=1.0,
        pos_cache=pos_cache,
        fast_train=True
    )
    # We don’t need df’s strategy.position because we use cached pos in WF
    rets = wf.run(df=df, params=params).dropna()
    if rets.empty or rets.std() == 0:
        m = {"n": 0, "mean": 0.0, "std": 0.0, "sharpe": 0.0, "cagr": 0.0, "max_dd": 0.0, "win_rate": 0.0}
    else:
        m = get_return_metrics(rets)
    return {
        "commission_bps": cbps,
        "slippage_bps": sbps,
        "stop_pct": stop,
        **m
    }

def run_cost_stop_sweep(cfg: SweepConfig) -> pd.DataFrame:
    # 1) Data once
    df = load_daily(cfg.symbol, cfg.start, None).copy()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0].lower() for c in df.columns]
    else:
        df = df.rename(columns=str.lower)
    assert "close" in df.columns, f"close column missing; got {df.columns.tolist()}"
    df = df.dropna(subset=["close"])

    # 2) Build grid once
    params = _build_param_grid(cfg.macd_grid)

    # 3) Precompute all MACD positions for grid once (major speedup)
    pos_cache = precompute_macd_positions(df, params)

    # 4) Windows
    train_window = int(252 * cfg.train_years)
    test_window  = int(21  * cfg.test_months)

    # 5) Parallel sweep over combos
    jobs = []
    rows = []
    combos = [(cbps, sbps, stop)
              for cbps in cfg.commission_bps_list
              for sbps in cfg.slippage_bps_list
              for stop in cfg.stop_list]

    # Use processes; pass compact objects (arrays in pos_cache are small)
    with ProcessPoolExecutor(max_workers=cfg.n_jobs) as ex:
        for (cbps, sbps, stop) in combos:
            jobs.append(ex.submit(
                _eval_combo, df, params, pos_cache, cbps, sbps, stop, train_window, test_window
            ))
        for f in as_completed(jobs):
            rows.append(f.result())

    out = pd.DataFrame(rows)
    # Usual sorting
    if not out.empty:
        out = out.sort_values(["sharpe", "cagr"], ascending=[False, False]).reset_index(drop=True)
    return out
