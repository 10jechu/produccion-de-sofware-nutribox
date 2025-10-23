import json
from starlette.requests import Request
from starlette.types import Message, Receive, Scope, Send

def _lowercase_keys(d: dict) -> dict:
    m = { (k.lower() if isinstance(k, str) else k): v for k, v in d.items() }
    # mapear nombre -> full_name si falta
    if "nombre" in m and "full_name" not in m:
        m["full_name"] = m["nombre"]
    return m

async def normalize_body_middleware(request: Request, call_next):
    try:
        ctype = request.headers.get("content-type", "")
        if request.method in {"POST","PUT","PATCH"} and ctype.startswith("application/json"):
            body_bytes = await request.body()
            if body_bytes:
                data = json.loads(body_bytes.decode("utf-8"))
                if isinstance(data, dict):
                    data = _lowercase_keys(data)
                elif isinstance(data, list):
                    data = [_lowercase_keys(x) if isinstance(x, dict) else x for x in data]
                new_body = json.dumps(data).encode("utf-8")

                async def receive() -> Message:
                    return {"type": "http.request", "body": new_body, "more_body": False}

                request = Request(request.scope, receive)
    except Exception:
        # Si algo falla, no bloqueamos la request; seguimos con el body original
        pass

    response = await call_next(request)
    return response
