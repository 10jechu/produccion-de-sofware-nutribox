#!/bin/bash
# =====================================================
# Ì∫Ä Test completo de CRUD NutriBox API v2
# Incluye pruebas: POST ‚Üí GET ‚Üí DELETE
# =====================================================

API_URL="http://127.0.0.1:8080/api/v1"
echo "Ì¥ç Iniciando pruebas completas de NutriBox API..."
echo "===================================================="

# --- Funci√≥n para mostrar t√≠tulos bonitos ---
section() {
  echo -e "\n\nÌ∑© $1"
  echo "----------------------------------------------------"
}

# --- 01 Usuarios ---
section "Usuarios"
USER_ID=$(curl -s -X POST "$API_URL/usuarios/" -H "Content-Type: application/json" \
  -d '{"nombre":"test_user","correo":"test@example.com","password":"1234"}' | jq -r '.id')
curl -s "$API_URL/usuarios/" | jq
curl -s "$API_URL/usuarios/$USER_ID" | jq
curl -s -X DELETE "$API_URL/usuarios/$USER_ID" | jq

# --- 02 Autenticaci√≥n ---
section "Auth"
curl -s -X POST "$API_URL/auth/" -H "Content-Type: application/json" \
  -d '{"usuario":"test_user","password":"1234"}' | jq

# --- 03 Direcciones ---
section "Direcciones"
DIR_ID=$(curl -s -X POST "$API_URL/direccions/" -H "Content-Type: application/json" \
  -d '{"direccion":"Calle 123","ciudad":"Bogot√°","usuario_id":1}' | jq -r '.id')
curl -s "$API_URL/direccions/" | jq
curl -s -X DELETE "$API_URL/direccions/$DIR_ID" | jq

# --- 04 Hijos ---
section "Hijos"
HIJO_ID=$(curl -s -X POST "$API_URL/hijos/" -H "Content-Type: application/json" \
  -d '{"nombre":"Juan","edad":10,"padre_id":1}' | jq -r '.id')
curl -s "$API_URL/hijos/" | jq
curl -s -X DELETE "$API_URL/hijos/$HIJO_ID" | jq

# --- 05 Loncheras ---
section "Loncheras"
LONCH_ID=$(curl -s -X POST "$API_URL/loncheras/" -H "Content-Type: application/json" \
  -d '{"nombre":"Lonchera Escolar","hijo_id":1}' | jq -r '.id')
curl -s "$API_URL/loncheras/" | jq
curl -s -X DELETE "$API_URL/loncheras/$LONCH_ID" | jq

# --- 06 Alimentos ---
section "Alimentos"
ALIM_ID=$(curl -s -X POST "$API_URL/alimentos/" -H "Content-Type: application/json" \
  -d '{"nombre":"Manzana","calorias":80}' | jq -r '.id')
curl -s "$API_URL/alimentos/" | jq
curl -s -X DELETE "$API_URL/alimentos/$ALIM_ID" | jq

# --- 07 Lonchera_Alimentos ---
section "Lonchera Alimentos"
LONCH_ALIM_ID=$(curl -s -X POST "$API_URL/lonchera_alimentos/" -H "Content-Type: application/json" \
  -d '{"lonchera_id":1,"alimento_id":1,"cantidad":2}' | jq -r '.id')
curl -s "$API_URL/lonchera_alimentos/" | jq
curl -s -X DELETE "$API_URL/lonchera_alimentos/$LONCH_ALIM_ID" | jq

# --- 08 Restricciones ---
section "Restricciones"
REST_ID=$(curl -s -X POST "$API_URL/restriccions/" -H "Content-Type: application/json" \
  -d '{"descripcion":"Sin gluten","usuario_id":1}' | jq -r '.id')
curl -s "$API_URL/restriccions/" | jq
curl -s -X DELETE "$API_URL/restriccions/$REST_ID" | jq

# --- 09 Excepciones ---
section "Excepciones"
EXC_ID=$(curl -s -X POST "$API_URL/excepcions/" -H "Content-Type: application/json" \
  -d '{"motivo":"Alergia temporal","usuario_id":1}' | jq -r '.id')
curl -s "$API_URL/excepcions/" | jq
curl -s -X DELETE "$API_URL/excepcions/$EXC_ID" | jq

# --- 10 Inventarios ---
section "Inventarios"
INV_ID=$(curl -s -X POST "$API_URL/inventarios/" -H "Content-Type: application/json" \
  -d '{"nombre":"Frutas","cantidad":50}' | jq -r '.id')
curl -s "$API_URL/inventarios/" | jq
curl -s -X DELETE "$API_URL/inventarios/$INV_ID" | jq

# --- 11 Movimientos de Inventario ---
section "Movimientos de Inventario"
MOV_ID=$(curl -s -X POST "$API_URL/inventario_movimientos/" -H "Content-Type: application/json" \
  -d '{"inventario_id":1,"tipo":"entrada","cantidad":10}' | jq -r '.id')
curl -s "$API_URL/inventario_movimientos/" | jq
curl -s -X DELETE "$API_URL/inventario_movimientos/$MOV_ID" | jq

# --- 12 Historial de Alimentos ---
section "Historial de Alimentos"
HIST_ID=$(curl -s -X POST "$API_URL/historial_alimentos/" -H "Content-Type: application/json" \
  -d '{"alimento_id":1,"fecha":"2025-10-21"}' | jq -r '.id')
curl -s "$API_URL/historial_alimentos/" | jq
curl -s -X DELETE "$API_URL/historial_alimentos/$HIST_ID" | jq

echo -e "\n‚úÖ Todas las pruebas CRUD completadas correctamente."
