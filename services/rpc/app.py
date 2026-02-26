from datetime import datetime, timezone
from fastapi import FastAPI, Request

app = FastAPI(title="quant-rpc", version="0.1.0")


@app.get("/healthz")
def healthz():
    return {"ok": True, "service": "quant-rpc"}


@app.post("/rpc")
async def rpc(request: Request):
    payload = await request.json()
    method = payload.get("method")
    params = payload.get("params", {})
    req_id = payload.get("id")

    try:
        result = dispatch(method, params)
        return {"jsonrpc": "2.0", "result": result, "id": req_id}
    except KeyError:
        return {"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": req_id}
    except Exception as exc:
        return {"jsonrpc": "2.0", "error": {"code": -32000, "message": str(exc)}, "id": req_id}


def dispatch(method: str, params: dict):
    methods = {
        "system.ping": system_ping,
        "backtest.status": backtest_status,
        "options.greeks": options_greeks,
    }
    if method not in methods:
        raise KeyError(method)
    return methods[method](params)


def system_ping(_: dict):
    return {"pong": True, "ts": datetime.now(timezone.utc).isoformat()}


def backtest_status(params: dict):
    run_id = params.get("run_id", "unknown")
    return {"run_id": run_id, "status": "placeholder", "note": "wire LEAN run state here"}


def options_greeks(params: dict):
    return {
        "symbol": params.get("symbol", "UNKNOWN"),
        "ts": datetime.now(timezone.utc).isoformat(),
        "delta": None,
        "gamma": None,
        "vega": None,
        "theta": None,
        "rho": None,
        "model": params.get("model", "bsm"),
        "note": "wire pricing engine in services/options-greeks",
    }
