# Data Pipeline Spec (Quant Lane)

## Goal
Provide reliable, replayable, and analyzable market data pipelines for MultiClaw research and trading operations.

## Stages
1. **Source acquisition** (LEAN/local/provider-based)
2. **Normalization** (symbol/timezone/session coherence)
3. **Validation** (schema and value constraints)
4. **Storage** (Postgres canonical tables)
5. **Access** (GraphQL + JSON-RPC)
6. **Monitoring** (lag, gaps, anomalies)

## Canonical entities
- `market.bars`
- `options.greeks_snapshot`
- `backtests.run_summary`

## Required quality checks
- timestamp monotonicity within symbol stream
- no duplicate natural keys
- data type and range validation
- session-window compliance using market-hours metadata

## Failure handling
- write failed records to quarantine log
- emit structured error context
- allow idempotent reprocessing
