# EXP_00 Baseline – MACD Walk-Forward Long Only

This baseline captures the current reproducible benchmark used for comparison
against future alpha research. It runs the walk-forward MACD long-only strategy
on the ^NSEI index with realistic costs and the filter stack used in production
(weekly trend, multi-bar confirmation, RSI, MFI, volume, ATR).

## How to reproduce

```bash
cd execution
pip install -r requirements.txt  # once, if running outside Docker
python jobs/run_baseline.py --config ../experiments/exp_00_baseline/config.yaml
```

When running via Docker Compose:

```bash
cd /Users/siddharthbhattacharya/quant-dual-stack
docker compose run --rm -T backtrader_exec python jobs/run_baseline.py \
  --config experiments/exp_00_baseline/config.yaml
```

## Outputs
- `results.csv`: Sharpe (net), CAGR, MaxDD, annualised vol, turnover, trades.
- `equity_curve.png`: cumulative equity curve (strategy vs buy & hold).
- `trade_log.parquet`: dated log of entries/exits with size, price, cost assumption.

## Assumptions
- Signals generated on the close are executed at next-day close (1-bar lag).
- Brokerage & slippage charged at 5 bps per side.
- Long-only; shorts suppressed by filters when MACD histogram turns negative.
- Weekly trend filter uses Friday resample of histogram.
