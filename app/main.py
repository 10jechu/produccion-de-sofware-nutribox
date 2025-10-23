from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.routes import api_router
from app.db.session import init_db

# Inicializar BD al importar
init_db()

app = FastAPI(
    title="NutriBox API",
    version="2.0.0",
    description="API para gestión de loncheras escolares"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "ok", "message": "NutriBox API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Incluir rutas
app.include_router(api_router, prefix="/api/v1")
