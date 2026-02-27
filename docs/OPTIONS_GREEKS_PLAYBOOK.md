# Options & Greeks Playbook 🦞

## Objective
Standardize how MultiClaw computes and uses option Greeks for decision support.

## Inputs
- underlying price/time series
- option chain (strike, expiry, right)
- implied volatility / surface assumptions
- rates/dividend assumptions

## Outputs
- `delta`, `gamma`, `vega`, `theta`, `rho`
- sensitivity surfaces for scenario analysis
- strategy-level aggregate greek exposure

## Workflow
1. Pull chain data from LEAN-supported paths.
2. Validate chain integrity and session context.
3. Compute/store snapshots in `options.greeks_snapshot`.
4. Run scenario shocks (spot/vol/time/rates).
5. Expose results in dashboard + API endpoints.

## Notes
- Keep model assumptions explicit per run.
- Store calculation provenance for reproducibility.
- Prefer conservative defaults for risk reporting.
