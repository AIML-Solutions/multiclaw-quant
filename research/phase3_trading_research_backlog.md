# Phase 3 Research Backlog — Trading Opportunities & Algo Codebases

## Objective
Continuously source, vet, and integrate high-signal strategy ideas + production-grade algorithm code into McOS.

## Evaluation rubric (must pass)
1. Reproducible historical backtest with transparent assumptions
2. Sensitivity tests (fees/slippage/latency/regime changes)
3. Out-of-sample validation period
4. Capacity constraints documented
5. Risk controls explicit (max DD, stop logic, exposure caps)

## Codebase vetting checklist
- License compatibility (MIT/Apache/BSD preferred)
- Active maintenance (commits/issues in last 6 months)
- Tests and CI present
- Clear data dependencies
- Avoid lookahead/data leakage patterns

## Candidate lanes
- Mean reversion (equities ETFs)
- Momentum/rotation (sector and index ETFs)
- Volatility-regime switching
- Options greeks overlays
- Event/news-driven alpha (from IntelliClaw signals)

## Top 5 validity gates
A top idea only qualifies when all are true:
- Sharpe > 1.2 in OOS
- Max drawdown < 15%
- Net profitability positive after fee+slippage stress
- Stability across at least 3 parameter perturbations
- Economic rationale can be stated in plain language

## Next research actions
- Build source catalog (repos/papers/forums/whitepapers)
- Standardize import of candidate algos into LEAN sandbox branch
- Auto-run baseline + stress backtests on import
- Score and store results into `backtests.run_summary`
- Surface ranked candidates in GraphQL leaderboard
