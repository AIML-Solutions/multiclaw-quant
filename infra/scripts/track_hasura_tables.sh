#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/aimls-dtd/.openclaw/workspace/projects/quantconnect/infra"
cd "$ROOT"
set -a; source .env; set +a

HASURA_URL="${HASURA_URL:-http://127.0.0.1:8080}"
SECRET="$HASURA_GRAPHQL_ADMIN_SECRET"
DB_SOURCE="default"

track() {
  local schema="$1"
  local table="$2"
  curl -sS "$HASURA_URL/v1/metadata" \
    -H "Content-Type: application/json" \
    -H "X-Hasura-Admin-Secret: $SECRET" \
    -d "{\"type\":\"pg_track_table\",\"args\":{\"source\":\"$DB_SOURCE\",\"table\":{\"schema\":\"$schema\",\"name\":\"$table\"}}}" >/tmp/hasura_track_resp.json || return 1
  cat /tmp/hasura_track_resp.json
}

TABLES=(
  "backtests run_summary"
  "brokerage accounts"
  "brokerage positions"
  "brokerage orders"
  "ingestion runs"
  "gos opportunities"
  "gos experiments"
  "gos daily_scoreboard"
  "gos improvement_log"
)

for t in "${TABLES[@]}"; do
  schema="${t%% *}"
  table="${t##* }"
  echo "Tracking $schema.$table"
  set +e
  out=$(track "$schema" "$table")
  rc=$?
  set -e
  if [[ $rc -ne 0 ]]; then
    echo "Failed to track $schema.$table"
  else
    echo "$out" | grep -q 'already tracked' && echo "already tracked" || true
  fi
done

echo "Done."
