#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/aimls-dtd/.openclaw/workspace/projects/quantconnect"
cd "$ROOT/infra"
set -a; source .env; set +a
export DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@127.0.0.1:5432/${POSTGRES_DB}"

cd "$ROOT/services/ingestion"
/bin/bash run_all_ingestors.sh
python3 promote_opportunities.py

echo "Phase 2 cycle complete"
