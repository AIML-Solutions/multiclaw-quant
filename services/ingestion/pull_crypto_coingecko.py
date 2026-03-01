#!/usr/bin/env python3
import json
import os
from datetime import datetime, timezone
from urllib import parse, request
import psycopg
from validation_models import MarketBarIn

DB_URL = os.getenv("DATABASE_URL", "postgresql://quant:quant_dev_change_me@127.0.0.1:5432/quant")
COINS = [c.strip().lower() for c in os.getenv("CRYPTO_COINS", "bitcoin,ethereum,solana").split(",") if c.strip()]
VS = os.getenv("CRYPTO_VS", "usd")


def fetch_market(ids):
    url = "https://api.coingecko.com/api/v3/coins/markets?" + parse.urlencode({
        "vs_currency": VS,
        "ids": ",".join(ids),
        "order": "market_cap_desc",
        "per_page": max(len(ids), 1),
        "page": 1,
        "sparkline": "false",
        "price_change_percentage": "24h",
    })
    with request.urlopen(url, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    ts = datetime.now(timezone.utc)
    rows = fetch_market(COINS)
    written = 0
    with psycopg.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("insert into ingestion.runs(source,run_type,status,metadata) values('coingecko','crypto_snapshot','started','{}'::jsonb) returning id")
            run_id = cur.fetchone()[0]
            for r in rows:
                symbol = (r.get("symbol") or "").upper() + "USD"
                price = r.get("current_price")
                mcap = r.get("market_cap")
                vol = r.get("total_volume")
                cur.execute(
                    """
                    insert into crypto.market_snapshot(symbol, ts, price_usd, market_cap_usd, volume_24h_usd, source, raw)
                    values (%s,%s,%s,%s,%s,'coingecko',%s::jsonb)
                    on conflict (symbol, ts) do update
                    set price_usd=excluded.price_usd, market_cap_usd=excluded.market_cap_usd,
                        volume_24h_usd=excluded.volume_24h_usd, raw=excluded.raw
                    """,
                    (symbol, ts, price, mcap, vol, json.dumps(r)),
                )
                try:
                    v = MarketBarIn(symbol=symbol, ts=ts, open=price, high=price, low=price, close=price, volume=vol or 0, source='coingecko')
                except Exception:
                    continue
                cur.execute(
                    """
                    insert into market.bars(symbol, ts, open, high, low, close, volume, source)
                    values (%s,%s,%s,%s,%s,%s,%s,'coingecko')
                    on conflict (symbol, ts) do update
                    set close=excluded.close, volume=excluded.volume, source=excluded.source
                    """,
                    (v.symbol, v.ts, v.open, v.high, v.low, v.close, v.volume),
                )
                written += 1
            cur.execute("update ingestion.runs set status='success', completed_at=now(), rows_written=%s where id=%s", (written, run_id))
        conn.commit()
    print(f"Coingecko ingest complete: {written}")


if __name__ == "__main__":
    main()
