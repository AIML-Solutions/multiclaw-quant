create schema if not exists analytics;

create or replace view analytics.ingestion_freshness_sla as
select
  source,
  max(started_at) as last_run_at,
  extract(epoch from (now() - max(started_at))) / 60.0 as minutes_since_last_run,
  case
    when extract(epoch from (now() - max(started_at))) / 60.0 > 90 then 'warn'
    else 'ok'
  end as sla_status
from ingestion.runs
group by source;

create or replace view analytics.selection_set_v1_executive as
select 'rates'::text as block, symbol, source, last_ts, last_close, last_volume
from analytics.selection_set_v1_latest_bars
where symbol in ('SOFR','MORTGAGE30US','DGS10','DGS2')
union all
select 'volatility'::text, symbol, source, last_ts, last_close, last_volume
from analytics.selection_set_v1_latest_bars
where symbol in ('VIXCLS','VXX','UVXY','SVXY')
union all
select 'equities_etf'::text, symbol, source, last_ts, last_close, last_volume
from analytics.selection_set_v1_latest_bars
where symbol in ('SPY','QQQ','IWM','DIA','VTI','TLT','IEF','XLF','XLK')
union all
select 'crypto'::text, symbol, source, last_ts, last_close, last_volume
from analytics.selection_set_v1_latest_bars
where symbol in ('BTCUSD','ETHUSD','SOLUSD');
