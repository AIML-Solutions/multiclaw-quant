# McOS v0.1 — Dataflow + GraphQL Integration Plan

## McOS meaning
McOS = **McOS MultiClaw Operating System**.

## Objective
Unify market/broker/backtest/intel/job data into PostgreSQL and expose it through Hasura GraphQL for queryable automation.

## What is now live
- PostgreSQL + Hasura + Qdrant running in `infra/docker-compose.yml`
- Backtest table: `backtests.run_summary`
- McOS tables: `gos.*`
- Broker ingestion tables: `brokerage.*` + `ingestion.runs`
- Backtest + ingest script: `lean/scripts/run_backtest_and_ingest.sh`
- Snapshot ingestion script: `services/ingestion/ingest_broker_snapshot.py`

## Data lanes
1. **QC/LEAN lane**
   - Strategy code in `lean-cli/<project>/main.py`
   - Run LEAN backtest
   - Ingest summary into `backtests.run_summary`

2. **Broker lane (Alpaca/Tradier paper first)**
   - Pull account/positions/orders API payloads
   - Normalize to snapshot JSON
   - Ingest into `brokerage.accounts|positions|orders`

3. **Opportunity lane**
   - Enrich market/news/jobs signals
   - Store actionable rows in `gos.opportunities`
   - Track execution outcomes in `gos.daily_scoreboard`

## GraphQL exposure (Hasura)
Track these schemas/tables in Hasura:
- `backtests.run_summary`
- `brokerage.accounts`
- `brokerage.positions`
- `brokerage.orders`
- `gos.opportunities`
- `gos.experiments`
- `gos.daily_scoreboard`
- `gos.improvement_log`
- `ingestion.runs`

Example query ideas:
- Latest paper positions by provider
- Backtest run leaderboard by Sharpe and drawdown
- New opportunities with confidence > 0.7 and status='new'
- Last failed ingestion runs

## GitHub algo code interoperability
Preferred pattern:
- Keep algorithm repos in `projects/*`
- Mirror/sync active algo modules into `projects/quantconnect/lean-cli/<project>/`
- Run `lean/scripts/run_backtest_and_ingest.sh <project>` after updates
- Store run metadata + source path in Postgres for traceability

## IDE workflow (Cursor/Windsurf/VS Code via SSH)
- Use local IDE remote SSH into VPS workspace
- Edit strategy code in git repo
- Sync into LEAN project path (or symlink where practical)
- Trigger backtest+ingest script
- Query results in Hasura GraphQL

## Next implementation targets
1. Add real Alpaca paper API puller (env-based token auth)
2. Add real Tradier paper API puller
3. Create scheduled ingestion jobs (cron + `ingestion.runs` health)
4. Add materialized views for strategy scorecards
5. Add GraphQL saved queries / dashboard preset
