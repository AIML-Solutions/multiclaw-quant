#!/usr/bin/env bash
set -euo pipefail
ROOT="/home/aimls-dtd/.openclaw/workspace/projects/quantconnect"
cd "$ROOT/infra"
set -a; source .env; set +a
export DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@127.0.0.1:5432/${POSTGRES_DB}"

cd "$ROOT/services/ingestion"
python3 pull_equities_bars_stooq.py || echo "stooq bars failed"
python3 pull_tradier_greeks.py || echo "tradier greeks failed"
python3 pull_crypto_coingecko.py || echo "coingecko failed"

echo "Phase 3.1 data lanes complete"
