create schema if not exists backtests;

create table if not exists backtests.run_summary (
  run_id text primary key,
  project text not null,
  started_at timestamptz,
  completed_at timestamptz default now(),
  end_equity numeric,
  net_profit_pct numeric,
  sharpe_ratio numeric,
  drawdown_pct numeric,
  total_orders integer,
  source_path text,
  raw_summary jsonb
);
