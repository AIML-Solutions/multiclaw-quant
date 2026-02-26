# Quant Division Scaffold

This workspace is the local QuantConnect + LEAN + data engineering stack for OpenClaw.

## Goals
- Run LEAN backtests/live workflows on this VPS.
- Ingest market data streams into PostgreSQL.
- Expose data via GraphQL (real-time capable) and JSON-RPC.
- Validate pipeline contracts using Pydantic.
- Support vectorized research/search workflows.
- Add blockchain analysis + Solidity/Hardhat section for on-chain quant tooling.

## Current Status
- LEAN CLI installed in user path (`~/.local/bin/lean`).
- Docker available.
- LEAN auth not completed yet (requires QuantConnect user id + API token).
- PostgreSQL/GraphQL stack scaffolded via docker-compose templates.

## Directory Map
- `lean/` — LEAN project/code/data layout
- `infra/` — docker-compose + DB bootstrap SQL
- `services/validation/` — Pydantic schema layer
- `services/rpc/` — JSON-RPC interface contracts
- `services/mcp/` — MCP integration notes/config stubs
- `services/options-greeks/` — options pricing framework notes
- `services/blockchain/` — smart-contract + chain-analysis area
- `docs/` — architecture and runbooks

## First Commands (manual)
```bash
# Add LEAN to your shell path (once)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Authenticate LEAN (interactive)
lean login
lean whoami
```

## Bring up core infra
```bash
cd projects/quantconnect/infra
cp .env.example .env
docker compose up -d
```

Then continue with `docs/architecture.md` and `docs/runbook.md`.
