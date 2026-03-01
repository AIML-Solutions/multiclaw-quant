create schema if not exists gos;

create table if not exists gos.opportunities (
  id bigserial primary key,
  detected_at timestamptz not null default now(),
  source text not null,                         -- market | news | jobs | manual
  category text not null,                       -- trading | intel | contract | automation
  title text not null,
  summary text,
  confidence numeric not null default 0.0,      -- 0..1
  expected_value_usd numeric,
  urgency text default 'normal',                -- low | normal | high | critical
  status text not null default 'new',           -- new | shortlisted | acted | rejected | expired
  expires_at timestamptz,
  metadata jsonb not null default '{}'::jsonb,
  unique(source, title, detected_at)
);

create index if not exists idx_gos_opportunities_status on gos.opportunities(status);
create index if not exists idx_gos_opportunities_category on gos.opportunities(category);
create index if not exists idx_gos_opportunities_detected_at on gos.opportunities(detected_at desc);

create table if not exists gos.experiments (
  id bigserial primary key,
  week_of date not null,
  lane text not null,                            -- market | intel | jobs | system
  name text not null,
  hypothesis text,
  metric text not null,
  target_value numeric,
  status text not null default 'planned',        -- planned | running | complete | failed
  notes text,
  created_at timestamptz not null default now(),
  completed_at timestamptz
);

create index if not exists idx_gos_experiments_week on gos.experiments(week_of);
create index if not exists idx_gos_experiments_status on gos.experiments(status);

create table if not exists gos.daily_scoreboard (
  day date primary key,
  opportunities_found int not null default 0,
  opportunities_acted int not null default 0,
  pnl_usd numeric,
  expected_value_delta_usd numeric,
  minutes_spent int,
  automation_failures int not null default 0,
  notes text,
  updated_at timestamptz not null default now()
);

create table if not exists gos.improvement_log (
  id bigserial primary key,
  logged_at timestamptz not null default now(),
  log_type text not null,                        -- win | failure | rule_change
  lane text not null default 'system',
  summary text not null,
  action_item text,
  source_ref text
);

create index if not exists idx_gos_improvement_log_type on gos.improvement_log(log_type);
create index if not exists idx_gos_improvement_log_logged_at on gos.improvement_log(logged_at desc);
