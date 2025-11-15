import requests
import time

def check_server():
    max_retries = 10
    for i in range(max_retries):
        try:
            response = requests.get("http://localhost:8000/", timeout=5)
            print(f"✅ Servidor funcionando! Status: {response.status_code}")
            return True
        except requests.exceptions.ConnectionError:
            print(f"⏳ Intentando conectar... ({i+1}/{max_retries})")
            time.sleep(2)
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    print("❌ No se pudo conectar al servidor después de varios intentos")
    print("   Asegúrate de que el servidor esté ejecutándose con: uvicorn app.main:app --reload --port 8000")
    return False

if __name__ == "__main__":
    check_server()
