create schema if not exists security;

create or replace view security.ingestion_anomalies as
select
  source,
  count(*) filter (where status='failed') as failed_runs,
  count(*) filter (where status='success') as success_runs,
  max(started_at) as last_run_at,
  round(avg(rows_written)::numeric,2) as avg_rows,
  case
    when count(*) filter (where status='failed') >= 3 then 'critical'
    when count(*) filter (where status='failed') >= 1 then 'warn'
    else 'ok'
  end as severity
from ingestion.runs
group by source;

create or replace view security.broker_order_anomalies as
select
  provider,
  account_id,
  count(*) filter (where status in ('rejected','canceled','expired')) as problematic_orders,
  count(*) as total_orders,
  max(updated_at) as last_order_at,
  case
    when count(*) filter (where status in ('rejected','canceled','expired')) >= 10 then 'critical'
    when count(*) filter (where status in ('rejected','canceled','expired')) >= 3 then 'warn'
    else 'ok'
  end as severity
from brokerage.orders
group by provider, account_id;
