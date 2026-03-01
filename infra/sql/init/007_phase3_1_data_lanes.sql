create schema if not exists crypto;

create table if not exists crypto.market_snapshot (
  symbol text not null,
  ts timestamptz not null,
  price_usd numeric,
  market_cap_usd numeric,
  volume_24h_usd numeric,
  source text not null default 'coingecko',
  raw jsonb not null default '{}'::jsonb,
  primary key (symbol, ts)
);

create index if not exists idx_crypto_market_snapshot_ts on crypto.market_snapshot(ts desc);
