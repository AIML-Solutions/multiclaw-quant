# Options Greeks & Pricing Framework (Open Source)

## Core Libraries to Evaluate
1. **QuantLib / QuantLib-Python**
   - Institutional-grade pricing models
   - Strong for term structures, vol surfaces, American options
2. **py_vollib**
   - Fast Black/Black-Scholes/BSM implied vol + Greeks
   - Great for production snapshots and sanity checks
3. **Mibian**
   - Lightweight educational/reference calculations
4. **NumPy/SciPy + custom models**
   - For Heston/SABR approximations or bespoke model research

## Proposed Model Stack
- **Tier 1 (production baseline):** Black-Scholes-Merton + finite-difference checks
- **Tier 2 (advanced):** Local vol / stochastic vol (Heston) for stress testing
- **Tier 3 (risk):** Scenario engine across spot/vol/rate shocks

## Data Dependencies
- Underlying spot / forward
- Strike, expiry, option type
- Rates curve
- Dividend assumptions
- IV surface snapshots

## Validation Rules
- Reject stale timestamps beyond tolerance window
- Cross-check implied vol inversion convergence
- Enforce no-arbitrage bounds where applicable

## Next implementation files
- `models.py` (pricing + Greeks interfaces)
- `calibration.py` (surface fitting)
- `risk_scenarios.py` (shock engine)
- `tests/` with benchmark vectors
