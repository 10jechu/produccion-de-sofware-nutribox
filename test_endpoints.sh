#!/bin/bash
# =====================================================
# Ì∫Ä Test autom√°tico de endpoints NutriBox API v2
# =====================================================
API_URL="http://127.0.0.1:8080/api/v1"

declare -A endpoints=(
  ["usuarios"]="Usuarios"
  ["auth"]="Autenticaci√≥n"
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

echo "Ì¥ç Iniciando pruebas autom√°ticas de endpoints..."
echo "==================================================="

for endpoint in "${!endpoints[@]}"; do
  name=${endpoints[$endpoint]}
  echo -e "\n‚û°Ô∏è  Probando $name..."

  echo "GET ‚Üí $API_URL/$endpoint/"
  curl -s -o /dev/null -w "%{http_code}" "$API_URL/$endpoint/" | xargs echo "C√≥digo HTTP:"
done

echo -e "\n‚úÖ Pruebas completadas."
