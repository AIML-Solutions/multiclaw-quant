#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path

import psycopg


def pct_to_float(value: str | None):
    if value is None:
        return None
    value = str(value).strip().replace('%', '').replace('$', '').replace(',', '')
    if value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def to_float(value: str | None):
    if value is None:
        return None
    value = str(value).strip().replace('$', '').replace(',', '')
    if value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def main():
    parser = argparse.ArgumentParser(description="Ingest LEAN backtest summary JSON into Postgres")
    parser.add_argument("summary_json", help="Path to *-summary.json")
    parser.add_argument("--project", default="baseline-strategy")
    args = parser.parse_args()

    summary_path = Path(args.summary_json).resolve()
    data = json.loads(summary_path.read_text())

    stats = data.get("statistics", {})
    state = data.get("state", {})
    run_id = summary_path.name.split("-")[0]

    started_at = state.get("StartTime")
    completed_at = state.get("EndTime")

    row = {
        "run_id": run_id,
        "project": args.project,
        "started_at": started_at,
        "completed_at": completed_at,
        "end_equity": to_float(stats.get("End Equity")),
        "net_profit_pct": pct_to_float(stats.get("Net Profit")),
        "sharpe_ratio": to_float(stats.get("Sharpe Ratio")),
        "drawdown_pct": pct_to_float(stats.get("Drawdown")),
        "total_orders": int(to_float(stats.get("Total Orders")) or 0),
        "source_path": str(summary_path),
        "raw_summary": json.dumps(data),
    }

    db_url = os.getenv("DATABASE_URL", "postgresql://quant:quant_dev_change_me@127.0.0.1:5432/quant")

    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                insert into backtests.run_summary (
                  run_id, project, started_at, completed_at,
                  end_equity, net_profit_pct, sharpe_ratio, drawdown_pct,
                  total_orders, source_path, raw_summary
                ) values (
                  %(run_id)s, %(project)s, %(started_at)s, %(completed_at)s,
                  %(end_equity)s, %(net_profit_pct)s, %(sharpe_ratio)s, %(drawdown_pct)s,
                  %(total_orders)s, %(source_path)s, %(raw_summary)s::jsonb
                )
                on conflict (run_id) do update set
                  project = excluded.project,
                  started_at = excluded.started_at,
                  completed_at = excluded.completed_at,
                  end_equity = excluded.end_equity,
                  net_profit_pct = excluded.net_profit_pct,
                  sharpe_ratio = excluded.sharpe_ratio,
                  drawdown_pct = excluded.drawdown_pct,
                  total_orders = excluded.total_orders,
                  source_path = excluded.source_path,
                  raw_summary = excluded.raw_summary
                """,
                row,
            )
        conn.commit()

    print(f"Ingested run_id={run_id} project={args.project} from {summary_path}")


if __name__ == "__main__":
    main()
