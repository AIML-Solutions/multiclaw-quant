create schema if not exists analytics;

create or replace function analytics.opportunity_score(confidence numeric, expected_value numeric, urgency text)
returns numeric
language sql
immutable
as $$
  select
    coalesce(confidence,0) * 0.55 +
    least(coalesce(expected_value,0) / 1000.0, 1.0) * 0.35 +
    case lower(coalesce(urgency,'normal'))
      when 'critical' then 0.10
      when 'high' then 0.07
      when 'normal' then 0.04
      else 0.02
    end;
$$;

create or replace view analytics.top_opportunities_now as
select
  o.id,
  o.detected_at,
  o.source,
  o.category,
  o.title,
  o.summary,
  o.confidence,
  o.expected_value_usd,
  o.urgency,
  o.status,
  analytics.opportunity_score(o.confidence, o.expected_value_usd, o.urgency) as score
from gos.opportunities o
where o.status in ('new','shortlisted')
order by score desc, detected_at desc
limit 5;

create schema if not exists orchestration;

create table if not exists orchestration.backtest_jobs (
  id bigserial primary key,
  created_at timestamptz not null default now(),
  source_opportunity_id bigint,
  project text not null default 'baseline-strategy',
  parameters jsonb not null default '{}'::jsonb,
  status text not null default 'queued', -- queued | running | complete | failed
  started_at timestamptz,
  completed_at timestamptz,
  result_run_id text,
  notes text
);

create index if not exists idx_backtest_jobs_status_created on orchestration.backtest_jobs(status, created_at);

create or replace function orchestration.enqueue_backtest_from_top_opps(min_score numeric default 0.65)
returns integer
language plpgsql
as $$
declare
  r record;
  inserted_count integer := 0;
begin
  for r in
    select * from analytics.top_opportunities_now where score >= min_score
  loop
    if r.category in ('trading','market') then
      insert into orchestration.backtest_jobs(source_opportunity_id, project, parameters, status, notes)
      values (
        r.id,
        'baseline-strategy',
        jsonb_build_object('symbol_hint', r.title, 'confidence', r.confidence, 'expected_value_usd', r.expected_value_usd),
        'queued',
        'Auto-enqueued from top_opportunities_now'
      );
      inserted_count := inserted_count + 1;
    end if;
  end loop;
  return inserted_count;
end;
$$;
