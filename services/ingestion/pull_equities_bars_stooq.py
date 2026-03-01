#!/usr/bin/env python3
import csv
import io
import os
from datetime import datetime, timezone
from urllib import request
import psycopg
from validation_models import MarketBarIn

DB_URL = os.getenv("DATABASE_URL", "postgresql://quant:quant_dev_change_me@127.0.0.1:5432/quant")
SYMBOLS = [s.strip().upper() for s in os.getenv("EQUITY_SYMBOLS", "SPY,QQQ,AAPL,MSFT").split(",") if s.strip()]


def fetch_stooq_daily(symbol: str):
    url = f"https://stooq.com/q/d/l/?s={symbol.lower()}.us&i=d"
    with request.urlopen(url, timeout=30) as r:
        text = r.read().decode("utf-8", errors="ignore")
    reader = csv.DictReader(io.StringIO(text))
    rows = list(reader)
    if not rows:
        return None
    last = rows[-1]
    if not last.get("Date"):
        return None
    dt = datetime.strptime(last["Date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return {
        "symbol": symbol,
        "ts": dt,
        "open": last.get("Open"),
        "high": last.get("High"),
        "low": last.get("Low"),
        "close": last.get("Close"),
        "volume": last.get("Volume") or 0,
    }


def main():
    written = 0
    with psycopg.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("insert into ingestion.runs(source,run_type,status,metadata) values('stooq','bars','started','{}'::jsonb) returning id")
            run_id = cur.fetchone()[0]

            for sym in SYMBOLS:
                row = fetch_stooq_daily(sym)
                if not row:
                    continue
                try:
                    v = MarketBarIn(**{**row, "source": "stooq"})
                except Exception:
                    continue
                cur.execute(
                    """
                    insert into market.bars(symbol, ts, open, high, low, close, volume, source)
                    values (%s,%s,%s,%s,%s,%s,%s,'stooq')
                    on conflict (symbol, ts) do update
                    set open=excluded.open, high=excluded.high, low=excluded.low, close=excluded.close, volume=excluded.volume, source=excluded.source
                    """,
                    (v.symbol, v.ts, v.open, v.high, v.low, v.close, v.volume),
                )
                written += 1

            cur.execute("update ingestion.runs set status='success', completed_at=now(), rows_written=%s where id=%s", (written, run_id))
        conn.commit()
    print(f"Stooq bars ingest complete: {written}")


if __name__ == "__main__":
    main()
