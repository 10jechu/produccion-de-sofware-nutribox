#!/usr/bin/env bash
set -euo pipefail

BASE="http://127.0.0.1:8080"

echo "â³ esperando a que levante la API..."
for i in {1..40}; do
  if curl -fsS "$BASE/health" >/dev/null 2>&1; then
    echo "âœ… API arriba"
    break
  fi
  sleep 0.5
done

echo "í´Ž rutas disponibles:"
curl -fsS "$BASE/openapi.json" | jq -r '.paths | keys | .[]' | sed 's/^/  - /'

echo "í±¤ creando usuario..."
curl -fsS -i -X POST "$BASE/api/v1/usuarios/" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Kewin","correo":"kewin@test.com","contrasena":"12345678"}' | sed -n '1,5p'

echo "í±¶ creando hijo..."
curl -fsS -i -X POST "$BASE/api/v1/hijos/" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Sofi","fecha_nacimiento":"2018-06-02","usuario_id":1}' | sed -n '1,5p'

echo "í½Ž creando alimento..."
curl -fsS -i -X POST "$BASE/api/v1/alimentos/" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Manzana","calorias":52,"unidad":"g"}' | sed -n '1,5p'

echo "í·ƒ creando lonchera..."
curl -fsS -i -X POST "$BASE/api/v1/loncheras/" \
  -H "Content-Type: application/json" \
  -d '{"hijo_id":1,"fecha":"2025-10-22"}' | sed -n '1,5p'

echo "âž• agregando alimento a lonchera..."
curl -fsS -i -X POST "$BASE/api/v1/lonchera_alimentos/" \
  -H "Content-Type: application/json" \
  -d '{"lonchera_id":1,"alimento_id":1,"cantidad":150}' | sed -n '1,5p'

echo "í³‹ listados finales:"
echo "  - usuarios:";            curl -fsS "$BASE/api/v1/usuarios/"            | jq .
echo "  - hijos:";               curl -fsS "$BASE/api/v1/hijos/"               | jq .
echo "  - alimentos:";           curl -fsS "$BASE/api/v1/alimentos/"           | jq .
echo "  - loncheras:";           curl -fsS "$BASE/api/v1/loncheras/"           | jq .
echo "  - lonchera_alimentos:";  curl -fsS "$BASE/api/v1/lonchera_alimentos/"  | jq .

echo "âœ… SMOKE OK"
