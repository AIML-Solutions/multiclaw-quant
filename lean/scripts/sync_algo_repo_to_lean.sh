#!/usr/bin/env bash
set -euo pipefail

# Sync external GitHub algo repo code into LEAN project folder.
# Usage:
#   bash sync_algo_repo_to_lean.sh /path/to/repo baseline-strategy [subdir]

SRC_REPO="${1:-}"
LEAN_PROJECT="${2:-baseline-strategy}"
SUBDIR="${3:-}"

if [[ -z "$SRC_REPO" ]]; then
  echo "Usage: $0 /path/to/repo baseline-strategy [subdir]" >&2
  exit 1
fi

ROOT="/home/aimls-dtd/.openclaw/workspace/projects/quantconnect"
DEST="$ROOT/lean-cli/$LEAN_PROJECT"

if [[ ! -d "$DEST" ]]; then
  echo "LEAN project not found: $DEST" >&2
  exit 1
fi

SRC="$SRC_REPO"
if [[ -n "$SUBDIR" ]]; then
  SRC="$SRC_REPO/$SUBDIR"
fi

if [[ ! -d "$SRC" ]]; then
  echo "Source path not found: $SRC" >&2
  exit 1
fi

rsync -av --delete \
  --exclude '.git' \
  --exclude '.venv' \
  --exclude '__pycache__' \
  --exclude 'node_modules' \
  "$SRC/" "$DEST/"

echo "Synced $SRC -> $DEST"
