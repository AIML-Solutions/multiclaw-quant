# LEAN Data Sources, Frequencies, and Market Hours (Initial Technical Rundown)

Generated from local LEAN data layout + market-hours database.

## 1) Asset classes detected in local LEAN data tree
- Equities (`equity/usa`, `equity/india`)
- Options (`option/usa`)
- Index options (`indexoption/usa`)
- Futures (`future/cme`, `future/comex`, `future/cbot`, ...)
- Future options (`futureoption/cme`, `futureoption/comex`)
- Crypto (`crypto/binance`, `crypto/coinbase`, `crypto/bybit`, ...)
- Crypto futures (`cryptofuture/binance`, `cryptofuture/bybit`, `cryptofuture/dydx`)
- Forex (`forex/oanda`, `forex/fxcm`)
- CFD (`cfd/oanda`)
- Index (`index/usa`, `index/eurex`, ...)

## 2) Frequency coverage (observed)
- Equities (USA): tick, second, minute, hour, daily
- Options (USA): minute, hour, daily + universes
- Index options (USA): minute, hour, daily + universes
- Futures (sample): minute/hour/daily; some include tick
- Crypto: minute/hour; coinbase includes second/daily
- Forex: tick, second, minute, hour, daily

## 3) Derivatives / Greeks source shape
### Option universe files
`data/option/usa/universes/<symbol>/<date>.csv`

Columns include:
- expiry, strike, right
- OHLC, volume, open_interest
- implied_volatility, delta, gamma, vega, theta, rho

This is a direct path for derivatives + Greeks analytics without additional paid feed for prototype workflows.

## 4) Market hours (from `market-hours-database.json`)
### Equity USA
- TZ: America/New_York
- Typical:
  - premarket: 04:00–09:30
  - market: 09:30–16:00
  - postmarket: 16:00–20:00

### Option USA
- TZ: America/New_York
- market: 09:30–16:00

### IndexOption USA
- data TZ: America/New_York, exchange TZ: America/Chicago
- market: 08:30–15:20

### Futures CME/COMEX (condensed)
- exchange TZ: America/Chicago, data TZ: UTC
- Sunday evening reopen + weekday near-continuous sessions with breaks

### Crypto (Binance/Coinbase)
- TZ: UTC
- 24/7 continuous market sessions

### Forex Oanda
- exchange TZ: America/New_York, data TZ: UTC
- near-24h weekdays with weekend close/reopen windows

## 5) Historical provider options exposed by LEAN CLI
`lean backtest --data-provider-historical` supports providers including:
- quantconnect
- local
- interactive brokers
- oanda
- bitfinex
- coinbase advanced trade
- binance
- kraken
- polygon
- alphavantage
- coinapi
- thetadata
- databento
- bybit
- dydx
- others

## 6) Recommended ingestion cadence (cost-aware)
- Minute bars for broad coverage baseline
- Second/tick only for narrow symbols and event windows
- Daily refresh for universe and EOD metrics
- Separate schedules by asset class/session windows using market-hours metadata

## 7) Notes on order-book depth
Local LEAN bundles above are largely trade/quote/bar-centric. Full L2 order-book depth generally requires dedicated providers/exchange APIs and should be piloted selectively to control cost/storage.
