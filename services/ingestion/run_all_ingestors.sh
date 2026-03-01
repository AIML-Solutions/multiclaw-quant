#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/aimls-dtd/.openclaw/workspace/projects/quantconnect"
cd "$ROOT/infra"
set -a; source .env; set +a
export DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@127.0.0.1:5432/${POSTGRES_DB}"

cd "$ROOT/services/ingestion"

if [[ -n "${ALPACA_API_KEY:-}" && -n "${ALPACA_API_SECRET:-}" ]]; then
  echo "Running Alpaca ingestor..."
  python3 pull_alpaca_paper.py || echo "Alpaca ingestor failed"
else
  echo "Skipping Alpaca ingestor (missing env vars)"
fi

if [[ -n "${TRADIER_API_TOKEN:-}" ]]; then
  echo "Running Tradier ingestor..."
  python3 pull_tradier_paper.py || echo "Tradier ingestor failed"
else
  echo "Skipping Tradier ingestor (missing env vars)"
fi

echo "Ingestor cycle complete"
