#!/usr/bin/env python3
"""Promote high-quality opportunities into experiments.
Rules:
- status = 'new'
- confidence >= threshold (default 0.70)
- expected_value_usd >= min_ev (default 50)
- not already promoted (metadata.promoted_to_experiment)
"""
import json
import os
import psycopg

DB_URL = os.getenv("DATABASE_URL", "postgresql://quant:quant_dev_change_me@127.0.0.1:5432/quant")
CONFIDENCE = float(os.getenv("GOS_PROMOTION_CONFIDENCE", "0.70"))
MIN_EV = float(os.getenv("GOS_PROMOTION_MIN_EV", "50"))


def main():
    promoted = 0
    with psycopg.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                select id, category, title, summary, confidence, expected_value_usd
                from gos.opportunities
                where status='new'
                  and coalesce(confidence,0) >= %s
                  and coalesce(expected_value_usd,0) >= %s
                  and coalesce((metadata->>'promoted_to_experiment')::boolean, false) = false
                order by detected_at desc
                limit 50
                """,
                (CONFIDENCE, MIN_EV),
            )
            rows = cur.fetchall()

            for (oid, category, title, summary, confidence, ev) in rows:
                lane = "system"
                if category in ("trading", "market"):
                    lane = "market"
                elif category in ("intel", "news"):
                    lane = "intel"
                elif category in ("contract", "jobs"):
                    lane = "jobs"

                cur.execute(
                    """
                    insert into gos.experiments(
                      week_of, lane, name, hypothesis, metric, target_value, status, notes
                    ) values (
                      date_trunc('week', now())::date,
                      %s,
                      %s,
                      %s,
                      'conversion_rate',
                      0.1,
                      'planned',
                      %s
                    )
                    """,
                    (lane, title[:180], summary or "Auto-promoted opportunity", f"confidence={confidence}, ev={ev}"),
                )
                cur.execute(
                    """
                    update gos.opportunities
                    set status='shortlisted',
                        metadata = coalesce(metadata,'{}'::jsonb) || %s::jsonb
                    where id=%s
                    """,
                    (json.dumps({"promoted_to_experiment": True}), oid),
                )
                promoted += 1

        conn.commit()
    print(f"Promoted opportunities: {promoted}")


if __name__ == "__main__":
    main()
