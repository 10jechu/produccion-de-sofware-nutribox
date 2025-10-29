# Contenido del archivo: app/main.py
# (Este es el código que ya tienes y está bien)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.database import Base, engine

# Importa los modelos para que SQLAlchemy los conozca
import app.db.models # noqa (Evita warnings de import no usado directamente)

# Crea las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

# Metadata para la documentación de Swagger/OpenAPI
tags_metadata = [
    {"name": "auth", "description": "1️⃣ Registro e inicio de sesion"},
    {"name": "users", "description": "2️⃣ Gestion de perfil de usuario"},
    {"name": "children", "description": "3️⃣ Gestion de hijos"},
    {"name": "addresses", "description": "4️⃣ Direcciones de envio"},
    {"name": "restrictions", "description": "5️⃣ Restricciones alimentarias"},
    {"name": "foods", "description": "6️⃣ Catalogo de alimentos"},
    {"name": "lunchboxes", "description": "7️⃣ Loncheras escolares"},
    {"name": "dev", "description": "🛠️ Endpoints de Desarrollo"}, # Añade si tienes el router dev
    {"name": "health", "description": "🩺 Health Check"},
]

# Crea la instancia principal de la aplicación FastAPI
app = FastAPI(
    title="NutriBox API",
    description="Plataforma para gestion de loncheras escolares - FASE 2",
    version="2.0.0",
    openapi_tags=tags_metadata # Usa la metadata definida arriba
)

# Configura CORS (Cross-Origin Resource Sharing) para permitir peticiones
# desde cualquier origen (tu frontend Vue.js)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite cualquier origen (ajusta en producción)
    allow_credentials=True,
    allow_methods=["*"], # Permite todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"], # Permite todas las cabeceras
)

# --- Endpoint de Health Check ---
# Una ruta simple para verificar que la API está funcionando
@app.get("/", tags=["health"])
def health():
    return {"status": "ok", "env": settings.ENV, "app": "NutriBox API v2.0"}

# --- Inclusión del Router Principal ---
# Importa el router que agrupa todos los demás routers de tu API v1
from app.api.v1.routes import api_router

# Incluye TODAS las rutas definidas en api_router (que a su vez incluye
# auth, users, children, etc.) bajo el prefijo /api/v1
app.include_router(api_router)

# (Opcional) Si tienes el router de desarrollo y quieres incluirlo también:
# from app.api.v1.routers import dev # Asegúrate de que exista
# app.include_router(dev.router) # Incluye las rutas /dev