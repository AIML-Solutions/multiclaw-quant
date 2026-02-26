# MCP Bridge Notes

Goal: surface quant capabilities as MCP tools consumable by OpenClaw.

## Initial MCP Tool Candidates
- `qc_backtest_run`
- `qc_backtest_status`
- `qc_get_greeks`
- `qc_graphql_query`
- `qc_chain_trace`

## Integration Approach
1. Implement JSON-RPC methods in `services/rpc`.
2. Add MCP adapter that maps tool calls -> JSON-RPC.
3. Add request validation + rate limits.
4. Log every request with correlation IDs.

## mcporter next-step
Use the `mcporter` skill to register a local MCP server once RPC methods exist.
