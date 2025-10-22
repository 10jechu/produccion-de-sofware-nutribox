from fastapi import FastAPI
from app.api.v1.routes import api_router
from app.db.session import init_db

app = FastAPI(title="NutriBox API", version="1.0.0")

# Inicializa BD (crea tablas si no existen)
init_db()

# Rutas v1
app.include_router(api_router)

# Healthcheck simple
@app.get("/health")
def health():
    return {"status": "ok"}
