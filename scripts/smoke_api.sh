#!/usr/bin/env bash
set -euo pipefail
BASE="http://127.0.0.1:8080"; JSON='Content-Type: application/json'
echo "Health:"; curl -s -i "$BASE/health" | head -n 1
TS=$(date +%s); USR_EMAIL="kew_${TS}@test.com"; USR_PASS="12345678"; FECHA_NAC="2018-06-02"; HOY="$(date +%Y-%m-%d)"

echo "Crear usuario"
RESP=$(curl -s -i -X POST "$BASE/api/v1/usuarios/" -H "$JSON" -d "{\"nombre\":\"Kew\",\"correo\":\"$USR_EMAIL\",\"contrasena\":\"$USR_PASS\"}")
echo "$RESP" | head -n1; echo "$RESP" | tail -n1

echo "Crear hijo"
RESP=$(curl -s -i -X POST "$BASE/api/v1/hijos/" -H "$JSON" -d "{\"nombre\":\"Sofi\",\"fecha_nacimiento\":\"$FECHA_NAC\",\"usuario_id\":1}")
echo "$RESP" | head -n1; echo "$RESP" | tail -n1

echo "Crear alimento"
RESP=$(curl -s -i -X POST "$BASE/api/v1/alimentos/" -H "$JSON" -d "{\"nombre\":\"Manzana\",\"calorias\":52,\"unidad\":\"g\"}")
echo "$RESP" | head -n1; echo "$RESP" | tail -n1

echo "Crear lonchera"
RESP=$(curl -s -i -X POST "$BASE/api/v1/loncheras/" -H "$JSON" -d "{\"hijo_id\":1,\"fecha\":\"$HOY\"}")
echo "$RESP" | head -n1; echo "$RESP" | tail -n1

echo "Agregar alimento a lonchera"
RESP=$(curl -s -i -X POST "$BASE/api/v1/lonchera_alimentos/" -H "$JSON" -d "{\"lonchera_id\":1,\"alimento_id\":1,\"cantidad\":150}")
echo "$RESP" | head -n1; echo "$RESP" | tail -n1
