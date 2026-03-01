#!/usr/bin/env python3
"""
Ingest broker account/positions/orders snapshots into PostgreSQL.

Usage:
  python3 ingest_broker_snapshot.py --provider alpaca --account-id ACCT1 --snapshot /path/snapshot.json

Expected snapshot JSON shape (flexible):
{
  "account": {"status":"ACTIVE","base_currency":"USD"},
  "positions": [{"symbol":"SPY","qty":1,"avg_entry_price":500.12,"market_price":502.0,"market_value":502.0,"unrealized_pl":1.88}],
  "orders": [{"id":"abc","symbol":"SPY","side":"buy","type":"market","status":"filled","qty":1,"filled_qty":1,"submitted_at":"...","updated_at":"..."}]
}
"""

import argparse
import json
import os
from datetime import datetime, timezone

import psycopg


def utcnow():
    return datetime.now(timezone.utc)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", required=True)
    ap.add_argument("--account-id", required=True)
    ap.add_argument("--mode", default="paper", choices=["paper", "live"])
    ap.add_argument("--snapshot", required=True)
    ap.add_argument("--db-url", default=os.getenv("DATABASE_URL", "postgresql://quant:quant_dev_change_me@127.0.0.1:5432/quant"))
    args = ap.parse_args()

    with open(args.snapshot, "r", encoding="utf-8") as f:
        payload = json.load(f)

    account = payload.get("account", {})
    positions = payload.get("positions", [])
    orders = payload.get("orders", [])
    as_of = payload.get("as_of") or utcnow().isoformat()

    with psycopg.connect(args.db_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                insert into ingestion.runs(source, run_type, status, started_at, metadata)
                values (%s, 'snapshot', 'started', now(), %s::jsonb)
                returning id
                """,
                (args.provider, json.dumps({"account_id": args.account_id, "mode": args.mode})),
            )
            run_id = cur.fetchone()[0]

            cur.execute(
                """
                insert into brokerage.accounts(provider, account_id, mode, base_currency, status, metadata, updated_at)
                values (%s,%s,%s,%s,%s,%s::jsonb, now())
                on conflict (provider, account_id) do update set
                  mode = excluded.mode,
                  base_currency = excluded.base_currency,
                  status = excluded.status,
                  metadata = excluded.metadata,
                  updated_at = now()
                """,
                (
                    args.provider,
                    args.account_id,
                    args.mode,
                    account.get("base_currency", "USD"),
                    account.get("status"),
                    json.dumps(account),
                ),
            )

            pcount = 0
            for p in positions:
                cur.execute(
                    """
                    insert into brokerage.positions(
                      provider, account_id, symbol, qty, avg_entry_price, market_price,
                      market_value, unrealized_pl, as_of, metadata
                    ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s::jsonb)
                    on conflict (provider, account_id, symbol, as_of) do update set
                      qty = excluded.qty,
                      avg_entry_price = excluded.avg_entry_price,
                      market_price = excluded.market_price,
                      market_value = excluded.market_value,
                      unrealized_pl = excluded.unrealized_pl,
                      metadata = excluded.metadata
                    """,
                    (
                        args.provider,
                        args.account_id,
                        p.get("symbol"),
                        p.get("qty", 0),
                        p.get("avg_entry_price"),
                        p.get("market_price"),
                        p.get("market_value"),
                        p.get("unrealized_pl"),
                        as_of,
                        json.dumps(p),
                    ),
                )
                pcount += 1

            ocount = 0
            for o in orders:
                order_id = o.get("id") or o.get("order_id")
                if not order_id:
                    continue
                cur.execute(
                    """
                    insert into brokerage.orders(
                      provider, account_id, order_id, symbol, side, order_type, status,
                      qty, filled_qty, submitted_at, updated_at, raw
                    ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s::jsonb)
                    on conflict (provider, account_id, order_id) do update set
                      symbol = excluded.symbol,
                      side = excluded.side,
                      order_type = excluded.order_type,
                      status = excluded.status,
                      qty = excluded.qty,
                      filled_qty = excluded.filled_qty,
                      submitted_at = excluded.submitted_at,
                      updated_at = excluded.updated_at,
                      raw = excluded.raw
                    """,
                    (
                        args.provider,
                        args.account_id,
                        order_id,
                        o.get("symbol"),
                        o.get("side"),
                        o.get("type") or o.get("order_type"),
                        o.get("status"),
                        o.get("qty"),
                        o.get("filled_qty"),
                        o.get("submitted_at"),
                        o.get("updated_at"),
                        json.dumps(o),
                    ),
                )
                ocount += 1

            cur.execute(
                """
                update ingestion.runs
                set status='success', completed_at=now(), rows_written=%s
                where id=%s
                """,
                (1 + pcount + ocount, run_id),
            )
        conn.commit()

    print(f"Ingested provider={args.provider} account={args.account_id} positions={pcount} orders={ocount}")


if __name__ == "__main__":
    main()
