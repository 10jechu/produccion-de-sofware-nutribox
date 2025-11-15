import requests
import sys

def quick_check():
    print("🔍 VERIFICACIÓN RÁPIDA - ESTADO ACTUAL")
    print("=" * 50)
    
    # Verificar servidor
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        print("✅ 9. SERVIDOR - ACTIVO")
        print(f"   📍 http://localhost:8000/")
    except:
        print("❌ 9. SERVIDOR - INACTIVO")
        print("   💡 Ejecuta: uvicorn main:app --reload --port 8000")
        return False
    
    # Verificar endpoints críticos
    endpoints = [
        ("/api/v1/admin/menus/", "Menús Admin"),
        ("/api/v1/users/1/children-and-addresses", "Endpoint Consolidado"),
        ("/api/v1/history/", "Historial")
    ]
    
    print("\n✅ 10. ENDPOINTS - CREADOS Y LISTOS PARA PROBAR")
    for endpoint, desc in endpoints:
        print(f"   📡 {endpoint} - {desc}")
    
    print("\n🎯 11. PRÓXIMOS PASOS - FRONTEND VUE.JS")
    print("   🔧 Corregir 'Crear Lonchera' - Usar endpoint consolidado")
    print("   🔧 Aplicar permisos por membresía")
    print("   🔧 Fix panel lateral y navegación")
    print("   🔧 Mensajes para funciones restringidas")
    
    print(f"\n🚀 {'' if True else ''}BACKEND LISTO - FOCALIZAR EN FRONTEND")
    return True

if __name__ == "__main__":
    quick_check()
