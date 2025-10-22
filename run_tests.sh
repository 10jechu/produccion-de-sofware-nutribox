#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# venv
if [ ! -f ".venv/Scripts/activate" ]; then
  python -m venv .venv
fi
source .venv/Scripts/activate

python -m pip install -U pip >/dev/null
test -f requirements.txt && python -m pip install -r requirements.txt || python -m pip install "fastapi[standard]" "uvicorn[standard]" pytest pytest-cov httpx pytest-asyncio sqlalchemy passlib-bcrypt >/dev/null

export PYTHONPATH="$(pwd)"

# levantar API
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --log-level warning &
UV_PID=$!
sleep 2

# health
curl -fsS http://127.0.0.1:8001/_health >/dev/null

# smoke auth
set +H
EMAIL="nutri_$(date +%s)@test.com"; PASSWORD='Nutri123!'
curl -fsS -X POST "http://127.0.0.1:8001/api/v1/dev/reset-db" >/dev/null || true
curl -fsS -X POST "http://127.0.0.1:8001/api/v1/dev/seed" >/dev/null || true
curl -fsS -X POST "http://127.0.0.1:8001/api/v1/auth/register" -H "Content-Type: application/json" -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\",\"nombre\":\"Demo User\"}" >/dev/null
TOKEN=$(python - <<PY
import json,sys,urllib.request,urllib.parse
data=urllib.parse.urlencode({"username":"$EMAIL","password":"$PASSWORD"}).encode()
resp=urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:8001/api/v1/auth/login", data=data), timeout=10).read().decode()
print(json.loads(resp)["access_token"])
PY
)

# pytest si hay tests
if [ -d tests ]; then
  python -m pytest -q --maxfail=1 --disable-warnings --cov=app --cov-report=term-missing
else
  echo "ℹ️  No hay carpeta tests; smoke test completado (AUTH OK)."
fi

kill $UV_PID 2>/dev/null || true
echo "✅ Fin ok"
