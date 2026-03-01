#!/usr/bin/env python3
import csv
import io
import os
from datetime import datetime, timezone
from urllib import request
import psycopg
from validation_models import MarketBarIn

DB_URL = os.getenv("DATABASE_URL", "postgresql://quant:quant_dev_change_me@127.0.0.1:5432/quant")
FRED_SERIES = [s.strip().upper() for s in os.getenv("FRED_SERIES", "SOFR,MORTGAGE30US,DGS10,DGS2,VIXCLS").split(",") if s.strip()]


def fetch_latest(series: str):
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}"
    with request.urlopen(url, timeout=30) as r:
        text = r.read().decode("utf-8", errors="ignore")
    rows = list(csv.DictReader(io.StringIO(text)))
    for row in reversed(rows):
        val = row.get(series)
        if val and val != '.':
            date_key = 'DATE' if 'DATE' in row else 'observation_date'
            dt = datetime.strptime(row[date_key], "%Y-%m-%d").replace(tzinfo=timezone.utc)
            return dt, float(val)
    return None, None


def main():
    written = 0
    with psycopg.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("insert into ingestion.runs(source,run_type,status,metadata) values('fred','macro','started','{}'::jsonb) returning id")
            run_id = cur.fetchone()[0]
            for s in FRED_SERIES:
                ts, val = fetch_latest(s)
                if ts is None:
                    continue
                try:
                    v = MarketBarIn(symbol=s, ts=ts, open=val, high=val, low=val, close=val, volume=0, source='fred')
                except Exception:
                    continue
                cur.execute(
                    """
                    insert into market.bars(symbol, ts, open, high, low, close, volume, source)
                    values (%s,%s,%s,%s,%s,%s,0,'fred')
                    on conflict (symbol, ts) do update
                    set close=excluded.close, source=excluded.source
                    """,
                    (v.symbol, v.ts, v.open, v.high, v.low, v.close),
                )
                written += 1
            cur.execute("update ingestion.runs set status='success', completed_at=now(), rows_written=%s where id=%s", (written, run_id))
        conn.commit()
    print(f"FRED macro ingest complete: {written}")


if __name__ == "__main__":
    main()
