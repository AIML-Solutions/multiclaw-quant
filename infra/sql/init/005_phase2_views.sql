create schema if not exists analytics;

create or replace view analytics.strategy_leaderboard as
select
  project,
  count(*) as runs,
  round(avg(coalesce(sharpe_ratio,0))::numeric, 4) as avg_sharpe,
  round(avg(coalesce(drawdown_pct,0))::numeric, 4) as avg_drawdown_pct,
  round(avg(coalesce(net_profit_pct,0))::numeric, 4) as avg_net_profit_pct,
  max(completed_at) as last_run_at
from backtests.run_summary
group by project
order by avg_sharpe desc nulls last;

create or replace view analytics.ingestion_health as
select
  source,
  count(*) filter (where status='success') as success_runs,
  count(*) filter (where status='failed') as failed_runs,
  max(started_at) as last_run_at,
  round(avg(rows_written)::numeric,2) as avg_rows_written
from ingestion.runs
group by source;

create or replace view analytics.opportunity_funnel as
select
  status,
  count(*) as count,
  round(avg(coalesce(confidence,0))::numeric,4) as avg_confidence,
  round(sum(coalesce(expected_value_usd,0))::numeric,2) as total_expected_value_usd
from gos.opportunities
group by status
order by count desc;
