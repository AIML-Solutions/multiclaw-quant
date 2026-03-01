create schema if not exists brokerage;
create schema if not exists ingestion;

create table if not exists brokerage.accounts (
  provider text not null,                         -- alpaca | tradier | ibkr | qc
  account_id text not null,
  mode text not null default 'paper',             -- paper | live
  base_currency text default 'USD',
  status text,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  primary key (provider, account_id)
);

create table if not exists brokerage.positions (
  provider text not null,
  account_id text not null,
  symbol text not null,
  qty numeric not null,
  avg_entry_price numeric,
  market_price numeric,
  market_value numeric,
  unrealized_pl numeric,
  as_of timestamptz not null,
  metadata jsonb not null default '{}'::jsonb,
  primary key (provider, account_id, symbol, as_of),
  foreign key (provider, account_id) references brokerage.accounts(provider, account_id)
);

create table if not exists brokerage.orders (
  provider text not null,
  account_id text not null,
  order_id text not null,
  symbol text,
  side text,
  order_type text,
  status text,
  qty numeric,
  filled_qty numeric,
  submitted_at timestamptz,
  updated_at timestamptz,
  raw jsonb not null default '{}'::jsonb,
  primary key (provider, account_id, order_id),
  foreign key (provider, account_id) references brokerage.accounts(provider, account_id)
);

create table if not exists ingestion.runs (
  id bigserial primary key,
  source text not null,                           -- alpaca | tradier | qc | manual
  run_type text not null,                         -- accounts | positions | orders | bars | backtest
  status text not null default 'started',         -- started | success | failed
  started_at timestamptz not null default now(),
  completed_at timestamptz,
  rows_written int not null default 0,
  error_text text,
  metadata jsonb not null default '{}'::jsonb
);

create index if not exists idx_ingestion_runs_source on ingestion.runs(source, started_at desc);
create index if not exists idx_brokerage_positions_asof on brokerage.positions(as_of desc);
