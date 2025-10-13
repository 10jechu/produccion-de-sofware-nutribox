from fastapi import FastAPI
from app.core.config import settings
from app.db.database import Base, engine
import app.db.models  # registra todos los modelos (Rol, Membresia, Usuario, Hijo, Alimento, ...)

# crea tablas en dev
Base.metadata.create_all(bind=engine)

app = FastAPI(title="NutriBox API")

@app.get("/")
def health():
    return {"status": "ok", "env": settings.ENV}

from app.api.v1.routes import api_router
app.include_router(api_router)
