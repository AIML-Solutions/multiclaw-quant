create schema if not exists market;
create schema if not exists options;
create schema if not exists research;

create table if not exists market.bars (
  symbol text not null,
  ts timestamptz not null,
  open numeric,
  high numeric,
  low numeric,
  close numeric,
  volume numeric,
  source text default 'lean',
  primary key (symbol, ts)
);

create table if not exists options.greeks_snapshot (
  underlying text not null,
  option_symbol text not null,
  ts timestamptz not null,
  price numeric,
  iv numeric,
  delta numeric,
  gamma numeric,
  vega numeric,
  theta numeric,
  rho numeric,
  model text,
  primary key (option_symbol, ts)
);

create table if not exists research.embeddings (
  id bigserial primary key,
  namespace text not null,
  ref_id text not null,
  content text,
  embedding_dim int,
  created_at timestamptz default now()
);
