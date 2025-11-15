echo \"🧪 PRUEBAS MANUALES CON CURL\"

echo \"1. 🔐 Login de admin:\"
curl -X POST \"http://localhost:8000/api/v1/auth/login\" ^
  -H \"Content-Type: application/x-www-form-urlencoded\" ^
  -d \"username=admin@nutribox.com&password=admin123\" ^
  -w \"\\nStatus: %{http_code}\\n\"

echo \"2. 📋 Listar menus (necesita token del paso 1):\"
echo \"Reemplaza TOKEN_AQUI con el token obtenido:\"
curl -X GET \"http://localhost:8000/api/v1/admin/menus/\" ^
  -H \"Authorization: Bearer TOKEN_AQUI\" ^
  -w \"\\nStatus: %{http_code}\\n\"

echo \"3. ➕ Crear menu (necesita token):\"
curl -X POST \"http://localhost:8000/api/v1/admin/menus/\" ^
  -H \"Authorization: Bearer TOKEN_AQUI\" ^
  -H \"Content-Type: application/json\" ^
  -d \"{\\\"nombre\\\":\\\"Menu Prueba\\\",\\\"descripcion\\\":\\\"Menu de prueba\\\",\\\"dia_semana\\\":\\\"Lunes\\\",\\\"alimentos\\\":[{\\\"alimento_id\\\":1,\\\"cantidad\\\":1}]}\" ^
  -w \"\\nStatus: %{http_code}\\n\"
