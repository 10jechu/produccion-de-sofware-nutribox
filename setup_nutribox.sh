#!/bin/bash

echo "í¼± Iniciando configuraciÃ³n completa de NutriBox API..."

# Crear estructura de carpetas
mkdir -p app/core
mkdir -p app/db/models
mkdir -p app/api/v1/routers
mkdir -p app/crud
mkdir -p app/schemas
mkdir -p scripts
mkdir -p tests

# Crear __init__.py en todas las carpetas
find app -type d -exec touch {}/__init__.py \;

# ======================================================
# í³¦ CONFIG.PY
# ======================================================
cat > app/core/config.py << 'PYCONF'
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "NutriBox API"
    VERSION: str = "1.0.0"
    DATABASE_URL: str = "sqlite:///./nutribox.db"
    ALLOWED_ORIGINS: list[str] = ["*"]
    SECRET_KEY: str = "dev-secret-key"

    class Config:
        env_file = ".env"

settings = Settings()
PYCONF

# ======================================================
# âš™ï¸ DATABASE.PY
# ======================================================
cat > app/db/database.py << 'PYDB'
from sqlmodel import SQLModel, create_engine
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
PYDB

# ======================================================
# í·  MAIN.PY
# ======================================================
cat > app/main.py << 'PYMAIN'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.database import create_db_and_tables
from app.api.v1.routers import auth, foods, lunchboxes, addresses, restrictions

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(auth.router, prefix="/api/v1", tags=["Auth"])
app.include_router(foods.router, prefix="/api/v1", tags=["Foods"])
app.include_router(lunchboxes.router, prefix="/api/v1", tags=["Lunchboxes"])
app.include_router(addresses.router, prefix="/api/v1", tags=["Addresses"])
app.include_router(restrictions.router, prefix="/api/v1", tags=["Restrictions"])

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
PYMAIN

# ======================================================
# í¼ ROUTERS
# ======================================================
declare -A ROUTERS=(
    ["auth"]="User registered / User logged in"
    ["foods"]="Food list / Create food"
    ["lunchboxes"]="Lunchbox list / Create lunchbox"
    ["addresses"]="Address list / Create address"
    ["restrictions"]="Restriction list / Create restriction"
)

for router in "${!ROUTERS[@]}"; do
cat > app/api/v1/routers/${router}.py << PYROUTER
from fastapi import APIRouter
router = APIRouter()

@router.get("/${router}")
def get_${router}():
    return {"${router}": "${ROUTERS[$router]}"}

@router.post("/${router}")
def create_${router}():
    return {"message": "${router^} created"}
PYROUTER
done

# ======================================================
# í·° DEPENDENCIAS
# ======================================================
echo "í³¦ Instalando dependencias requeridas..."
pip install fastapi uvicorn sqlmodel sqlalchemy pydantic-settings

# ======================================================
# íº€ EJECUTAR SERVIDOR
# ======================================================
echo "âœ… ConfiguraciÃ³n completada correctamente."
echo "í¼ Iniciando servidor en http://127.0.0.1:8080 ..."
uvicorn app.main:app --reload --port 8080
