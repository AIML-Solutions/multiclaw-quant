# JSON-RPC Layer (Planned)

Purpose: expose deterministic quant operations for OpenClaw/MCP without overloading GraphQL.

## Candidate Methods
- `backtest.run(project, start, end, params)`
- `backtest.status(run_id)`
- `market.bars(symbol, resolution, from, to)`
- `options.greeks(symbol, ts, model)`
- `signals.latest(strategy)`

## Recommended Stack
- FastAPI transport + JSON-RPC 2.0 method handlers
- Pydantic request/response schemas
- Auth via local token or mTLS on private network

## Why both GraphQL and JSON-RPC?
- GraphQL: flexible read/query layer (dashboards + analysts)
- JSON-RPC: strict command/action interface (agents + automation)
