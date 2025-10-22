#!/bin/bash
# =====================================================
# � Test automático de endpoints NutriBox API v2
# =====================================================
API_URL="http://127.0.0.1:8080/api/v1"

declare -A endpoints=(
  ["usuarios"]="Usuarios"
  ["auth"]="Autenticación"
  ["direccions"]="Direcciones"
  ["hijos"]="Hijos"
  ["loncheras"]="Loncheras"
  ["alimentos"]="Alimentos"
  ["lonchera_alimentos"]="Lonchera Alimentos"
  ["restriccions"]="Restricciones"
  ["excepcions"]="Excepciones"
  ["inventarios"]="Inventarios"
  ["inventario_movimientos"]="Movimientos de Inventario"
  ["historial_alimentos"]="Historial de Alimentos"
)

echo "� Iniciando pruebas automáticas de endpoints..."
echo "==================================================="

for endpoint in "${!endpoints[@]}"; do
  name=${endpoints[$endpoint]}
  echo -e "\n➡️  Probando $name..."

  echo "GET → $API_URL/$endpoint/"
  curl -s -o /dev/null -w "%{http_code}" "$API_URL/$endpoint/" | xargs echo "Código HTTP:"
done

echo -e "\n✅ Pruebas completadas."
