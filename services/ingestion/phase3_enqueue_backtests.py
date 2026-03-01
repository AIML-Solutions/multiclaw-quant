#!/usr/bin/env python3
import os
import psycopg

DB_URL = os.getenv("DATABASE_URL", "postgresql://quant:quant_dev_change_me@127.0.0.1:5432/quant")
MIN_SCORE = float(os.getenv("GOS_BACKTEST_ENQUEUE_MIN_SCORE", "0.65"))


def main():
    with psycopg.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("select orchestration.enqueue_backtest_from_top_opps(%s::numeric)", (MIN_SCORE,))
            inserted = cur.fetchone()[0]
        conn.commit()
    print(f"Enqueued backtest jobs: {inserted}")


if __name__ == "__main__":
    main()
