-- Data sanity constraints (additive, low-risk)

-- gos.opportunities: confidence in [0,1], expected value non-negative when present
alter table gos.opportunities
  add constraint gos_opportunities_confidence_range_chk
  check (confidence >= 0 and confidence <= 1) not valid;

alter table gos.opportunities
  add constraint gos_opportunities_expected_value_nonnegative_chk
  check (expected_value_usd is null or expected_value_usd >= 0) not valid;

-- market.bars: non-negative volume, positive prices
alter table market.bars
  add constraint market_bars_volume_nonnegative_chk
  check (volume >= 0) not valid;

alter table market.bars
  add constraint market_bars_prices_positive_chk
  check (open > 0 and high > 0 and low > 0 and close > 0) not valid;

-- options.greeks_snapshot: sensible ranges where populated
alter table options.greeks_snapshot
  add constraint options_greeks_iv_nonnegative_chk
  check (iv is null or iv >= 0) not valid;

alter table options.greeks_snapshot
  add constraint options_greeks_delta_range_chk
  check (delta is null or (delta >= -1 and delta <= 1)) not valid;

-- brokerage.positions/orders: quantities non-negative
alter table brokerage.positions
  add constraint brokerage_positions_qty_nonnegative_chk
  check (qty >= 0) not valid;

alter table brokerage.orders
  add constraint brokerage_orders_qty_nonnegative_chk
  check ((qty is null or qty >= 0) and (filled_qty is null or filled_qty >= 0)) not valid;

-- Validate constraints against current data (safe after add)
alter table gos.opportunities validate constraint gos_opportunities_confidence_range_chk;
alter table gos.opportunities validate constraint gos_opportunities_expected_value_nonnegative_chk;
alter table market.bars validate constraint market_bars_volume_nonnegative_chk;
alter table market.bars validate constraint market_bars_prices_positive_chk;
alter table options.greeks_snapshot validate constraint options_greeks_iv_nonnegative_chk;
alter table options.greeks_snapshot validate constraint options_greeks_delta_range_chk;
alter table brokerage.positions validate constraint brokerage_positions_qty_nonnegative_chk;
alter table brokerage.orders validate constraint brokerage_orders_qty_nonnegative_chk;
