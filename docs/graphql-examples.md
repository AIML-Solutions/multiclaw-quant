# GraphQL Examples (Hasura)

Endpoint: `http://localhost:8080/v1/graphql`
Header: `x-hasura-admin-secret: <HASURA_GRAPHQL_ADMIN_SECRET>`

## Query latest bars
```graphql
query LatestBars($symbol: String!) {
  market_bars(where: {symbol: {_eq: $symbol}}, order_by: {ts: desc}, limit: 50) {
    symbol
    ts
    open
    high
    low
    close
    volume
  }
}
```

## Query latest greeks snapshot
```graphql
query LatestGreeks($underlying: String!) {
  options_greeks_snapshot(
    where: {underlying: {_eq: $underlying}}
    order_by: {ts: desc}
    limit: 50
  ) {
    underlying
    option_symbol
    ts
    iv
    delta
    gamma
    vega
    theta
    rho
    model
  }
}
```

## Subscription (realtime) for bars
```graphql
subscription BarsLive($symbol: String!) {
  market_bars(where: {symbol: {_eq: $symbol}}, order_by: {ts: desc}, limit: 1) {
    symbol
    ts
    close
  }
}
```
