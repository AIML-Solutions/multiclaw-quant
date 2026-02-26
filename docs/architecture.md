# Quant System Architecture (Open Source / Free-Tier Friendly)

## Core Principles
1. **Local-first and auditable**: self-host on VPS with Docker.
2. **Composable interfaces**: Postgres as source of truth, GraphQL for clients, JSON-RPC for internal agents/tools.
3. **Strict data contracts**: Pydantic validation before writes.
4. **Realtime where useful**: GraphQL subscriptions for dashboards.
5. **Agent-friendly**: MCP endpoints and filesystem conventions optimized for OpenClaw.

## Proposed Stack
- **Execution/Backtesting**: QuantConnect LEAN CLI + Docker engine.
- **Primary DB**: PostgreSQL 16 (open source).
- **GraphQL**: Hasura (real-time GraphQL over Postgres).
- **Vector Store**: Qdrant (open-source vector DB).
- **Validation Layer**: Python + Pydantic v2.
- **RPC Layer**: JSON-RPC 2.0 service (FastAPI transport, JSON-RPC methods).
- **Agent Tooling**: MCP bridge docs/config in `services/mcp`.
- **Blockchain Quant Sidecar**: Hardhat + Solidity + chain-tracing scripts.

## Data Flow (Initial)
1. LEAN backtest/live run emits results and artifacts.
2. Ingestion script normalizes output into canonical schema.
3. Pydantic validation enforces type + integrity checks.
4. Data written to Postgres (`market`, `options`, `signals`, `backtests`).
5. Hasura exposes query + subscriptions for dashboards/agents.
6. Research text/features embedded and stored in Qdrant for retrieval.

## Why this works well with OpenClaw
- SQL and GraphQL are both agent-friendly and introspectable.
- JSON-RPC methods can be wrapped as MCP tools.
- Clear folder partitioning lowers cognitive load for multi-agent workflows.

## Next Milestones
1. Complete LEAN authentication (`lean login`).
2. Launch infra stack (`docker compose up`).
3. Define initial Postgres schema and migrations.
4. Implement ingestion + validation skeleton.
5. Add first GraphQL queries/subscriptions for live metrics.
6. Add options greeks model package and first pricing API.
