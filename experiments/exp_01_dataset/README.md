# EXP_01 Dataset Builder

Configuration used for building the cross-sectional daily dataset (Phase 1).

- Universe: starter list of NIFTY50 names + ^NSEI index (placeholder until survivor-free universe is wired).
- Start date: 2015-01-01 (buffer of 250 days automatically added for rolling windows).
- Outputs:
  - `data/features.parquet`
  - `data/labels.parquet`
  - `data/meta.json`

Run:

```bash
cd /Users/siddharthbhattacharya/quant-dual-stack
docker compose run --rm -T \
  -v "$(pwd)/experiments:/app/experiments" \
  backtrader_exec \
  python /app/jobs/build_ml_dataset.py --config /app/experiments/exp_01_dataset/config.yaml
```

Outputs are git-ignored by default (see `.gitignore`).
