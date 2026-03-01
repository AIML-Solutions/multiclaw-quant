#!/usr/bin/env python3
import json
import os
from datetime import datetime, timezone
from urllib import parse, request
import psycopg
from validation_models import GreeksIn

DB_URL = os.getenv("DATABASE_URL", "postgresql://quant:quant_dev_change_me@127.0.0.1:5432/quant")
TRADIER_BASE = os.getenv("TRADIER_SANDBOX_BASE_URL") or os.getenv("TRADIER_PAPER_BASE_URL") or "https://sandbox.tradier.com/v1"
TRADIER_TOKEN = os.getenv("TRADIER_SANDBOX_TOKEN") or os.getenv("TRADIER_API_TOKEN") or os.getenv("TRADIER_LIVE_TOKEN")
UNDERLYINGS = [s.strip().upper() for s in os.getenv("OPTIONS_SYMBOLS", "SPY,QQQ").split(",") if s.strip()]
EXPIRATION = os.getenv("OPTIONS_EXPIRATION", "")


def get_json(path, query=None):
    url = TRADIER_BASE.rstrip("/") + path
    if query:
        url += "?" + parse.urlencode(query)
    req = request.Request(url)
    req.add_header("Authorization", f"Bearer {TRADIER_TOKEN}")
    req.add_header("Accept", "application/json")
    with request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    if not TRADIER_TOKEN:
        raise SystemExit("Missing Tradier token")

    written = 0
    now = datetime.now(timezone.utc)
    with psycopg.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("insert into ingestion.runs(source,run_type,status,metadata) values('tradier','greeks','started','{}'::jsonb) returning id")
            run_id = cur.fetchone()[0]

            for sym in UNDERLYINGS:
                exp = EXPIRATION
                if not exp:
                    exps = get_json(f"/markets/options/expirations", {"symbol": sym, "includeAllRoots": "true", "strikes": "false"})
                    dates = exps.get("expirations", {}).get("date") if isinstance(exps, dict) else None
                    if isinstance(dates, list) and dates:
                        exp = dates[0]
                    elif isinstance(dates, str):
                        exp = dates
                    else:
                        continue

                chain = get_json(f"/markets/options/chains", {"symbol": sym, "expiration": exp, "greeks": "true"})
                options = chain.get("options", {}).get("option") if isinstance(chain, dict) else None
                if isinstance(options, dict):
                    options = [options]
                if not isinstance(options, list):
                    continue

                for o in options[:150]:
                    greeks = o.get("greeks") or {}
                    try:
                        g = GreeksIn(
                            underlying=sym,
                            option_symbol=o.get("symbol") or "",
                            ts=now,
                            price=o.get("last") or o.get("bid") or o.get("ask") or 0,
                            iv=greeks.get("mid_iv") or greeks.get("smv_vol"),
                            delta=greeks.get("delta"),
                            gamma=greeks.get("gamma"),
                            vega=greeks.get("vega"),
                            theta=greeks.get("theta"),
                            rho=greeks.get("rho"),
                            model='tradier'
                        )
                    except Exception:
                        continue
                    cur.execute(
                        """
                        insert into options.greeks_snapshot(
                          underlying, option_symbol, ts, price, iv, delta, gamma, vega, theta, rho, model
                        ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'tradier')
                        on conflict (option_symbol, ts) do update
                        set price=excluded.price, iv=excluded.iv, delta=excluded.delta, gamma=excluded.gamma,
                            vega=excluded.vega, theta=excluded.theta, rho=excluded.rho, model=excluded.model
                        """,
                        (g.underlying, g.option_symbol, g.ts, g.price,
                         g.iv, g.delta, g.gamma,
                         g.vega, g.theta, g.rho),
                    )
                    written += 1

            cur.execute("update ingestion.runs set status='success', completed_at=now(), rows_written=%s where id=%s", (written, run_id))
        conn.commit()
    print(f"Tradier greeks ingest complete: {written}")


if __name__ == "__main__":
    main()
