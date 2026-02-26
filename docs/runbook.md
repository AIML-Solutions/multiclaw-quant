# Quant Runbook (Phase 1)

## 0) Preconditions
- Docker installed and running ✅
- LEAN CLI installed ✅ (`~/.local/bin/lean`)
- QuantConnect credentials available (user id + API token) ⏳

## 1) Authenticate LEAN
```bash
export PATH="$HOME/.local/bin:$PATH"
lean login
lean whoami
```

## 2) Initialize LEAN workspace
Run inside `projects/quantconnect/lean` after login:
```bash
cd ~/.openclaw/workspace/projects/quantconnect/lean
lean init --language python
lean project-create "baseline-strategy" --language python
```

## 3) Start DB + GraphQL + Vector
```bash
cd ~/.openclaw/workspace/projects/quantconnect/infra
cp .env.example .env
docker compose up -d
```

## 4) Verify services
- Postgres: `localhost:5432`
- Hasura GraphQL: `http://localhost:8080/v1/graphql`
- Qdrant: `http://localhost:6333`

## 5) Ingestion / validation loop
- Build scripts under `lean/scripts` to parse LEAN output.
- Validate payloads with models in `services/validation/models.py`.
- Insert into Postgres using idempotent upserts.

## 6) Expose agent interfaces
- GraphQL for dashboards/realtime queries.
- JSON-RPC methods for deterministic internal actions.
- MCP wrappers for agent-side tool calling.

## 7) Security + cost controls
- Keep secrets in `.env` only, never in git.
- Use least-privilege DB user for write jobs.
- Track model/billing status from OpenClaw before long jobs.

## 8) Expand to blockchain quant lane
- Initialize Hardhat project in `services/blockchain/hardhat`.
- Add chain-tracing jobs to `services/blockchain/analysis`.
