# MultiClaw Quant

**MultiClaw Quant** is the quantitative engineering lane for AIML Solutions.

It combines QuantConnect LEAN, structured data ingestion, options/greeks analytics, and query interfaces for downstream agents and dashboards.

## What this repo delivers

- LEAN backtest/research execution workflows
- Market data ingestion and validation (Pydantic/Pandera-ready)
- PostgreSQL schema for bars, greeks snapshots, and backtest summaries
- GraphQL access via Hasura
- JSON-RPC + MCP integration path for agent tooling
- Adjacent blockchain quant lane (Hardhat + chain analysis staging)

## Current status

- LEAN authenticated and baseline strategy backtests validated
- Quant infra stack running: Postgres + Hasura + Qdrant
- Backtest summary ingestion into Postgres verified
- GraphQL query path validated
- Market-hours and data-source guide documented

## Key docs

- [`docs/architecture.md`](docs/architecture.md)
- [`docs/runbook.md`](docs/runbook.md)
- [`docs/data-sources-and-market-hours.md`](docs/data-sources-and-market-hours.md)
- [`docs/graphql-examples.md`](docs/graphql-examples.md)

## Quick start

```bash
# 1) LEAN auth
lean login
lean whoami

# 2) Start core quant infra
cd infra
cp .env.example .env
docker compose up -d

# 3) Run a local backtest (example)
cd ../lean-cli
lean backtest "baseline-strategy" --no-update
```

## Core directories

- `lean-cli/` — LEAN projects and backtest outputs
- `lean/` — scripts/utilities for setup and ingestion
- `infra/` — docker compose and SQL bootstrap
- `services/validation/` — data model contracts
- `services/rpc/` — JSON-RPC service scaffold
- `services/mcp/` — MCP integration notes
- `services/options-greeks/` — pricing/greeks framework notes
- `services/blockchain/` — chain analytics/dev lane linkage

## License

MIT — see [LICENSE](LICENSE).
