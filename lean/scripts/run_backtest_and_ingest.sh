#!/usr/bin/env bash
set -euo pipefail

# Run a LEAN backtest, then ingest latest summary into Postgres.
# Usage: bash run_backtest_and_ingest.sh [project-name]

PROJECT="${1:-baseline-strategy}"
ROOT="/home/aimls-dtd/.openclaw/workspace/projects/quantconnect"
LEAN_CLI="$ROOT/lean-cli"
INGEST_PY="$ROOT/lean/scripts/ingest_backtest_summary.py"

export PATH="$HOME/.local/bin:$PATH"

cd "$LEAN_CLI"
lean backtest "$PROJECT" --no-update

LATEST_SUMMARY=$(find "$LEAN_CLI/$PROJECT/backtests" -type f -name '*-summary.json' | sort | tail -n 1)
if [[ -z "$LATEST_SUMMARY" ]]; then
  echo "No summary file found for $PROJECT" >&2
  exit 1
fi

python3 "$INGEST_PY" "$LATEST_SUMMARY" --project "$PROJECT"

echo "Backtest + ingest complete for $PROJECT"
