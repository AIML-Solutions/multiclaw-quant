create schema if not exists analytics;

create or replace view analytics.selection_set_v1_latest_bars as
with ranked as (
  select
    symbol,
    source,
    ts,
    close,
    volume,
    row_number() over (partition by symbol, source order by ts desc) as rn
  from market.bars
  where symbol in (
    'SPY','QQQ','IWM','DIA','VTI','TLT','IEF','XLF','XLK',
    'VXX','UVXY','SVXY','BTCUSD','ETHUSD','SOLUSD',
    'SOFR','MORTGAGE30US','DGS10','DGS2','VIXCLS'
  )
)
select symbol, source, ts as last_ts, close as last_close, volume as last_volume
from ranked
where rn = 1;

create or replace view analytics.selection_set_v1_options_greeks as
select
  underlying,
  count(*) as contracts,
  max(ts) as last_ts,
  round(avg(coalesce(delta,0))::numeric, 6) as avg_delta,
  round(avg(coalesce(gamma,0))::numeric, 6) as avg_gamma,
  round(avg(coalesce(vega,0))::numeric, 6) as avg_vega,
  round(avg(coalesce(theta,0))::numeric, 6) as avg_theta
from options.greeks_snapshot
where underlying in ('SPY','QQQ','IWM','TLT')
group by underlying
order by underlying;
