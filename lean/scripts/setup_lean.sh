#!/usr/bin/env bash
set -euo pipefail

export PATH="$HOME/.local/bin:$PATH"

if ! command -v lean >/dev/null 2>&1; then
  echo "lean CLI not found in PATH. Expected at ~/.local/bin/lean"
  exit 1
fi

echo "LEAN version: $(lean --version)"

WHOAMI_OUTPUT="$(lean whoami 2>&1 || true)"
if echo "$WHOAMI_OUTPUT" | grep -qi "not logged in"; then
  echo "LEAN not authenticated. Run: lean login"
else
  echo "LEAN already authenticated."
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ ! -f lean.json ]]; then
  echo "No lean.json found. After login run: lean init --language python"
else
  echo "lean.json already exists."
fi
