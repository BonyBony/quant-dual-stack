# EXP_01 Dataset Builder

Configuration for Phase 1 (data + labels) using the modular feature blocks.

## Inputs
- Start date: 2015-01-01 (250-day buffer automatically used for rolling windows)
- Universe: `research/config/nifty_universe.txt` (starter NIFTY list; replace with survivor-free list when ready)
- Feature config: `research/config/features.yaml`

## Outputs
- `data/features.parquet`
- `data/labels.parquet`
- `data/meta.json`
- `data/feature_corr.png`

## Run
```bash
cd /Users/siddharthbhattacharya/quant-dual-stack
docker compose run --rm -T \
  -v "$(pwd)/experiments:/app/experiments" \
  -v "$(pwd)/research:/app/research" \
  backtrader_exec \
  python /app/jobs/build_ml_dataset.py \
    --config /app/experiments/exp_01_dataset/config.yaml
```
(Feature config path can be overridden with `--feature-config`.)

Outputs are git-ignored by default.
