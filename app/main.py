from fastapi import FastAPI
from app.api.v1.routers import routes as api_v1_routes
from app.core.deps import get_db

app = FastAPI(title="NutriBox API", version="1.0.0")

# Incluir todos los routers de la API v1
app.include_router(api_v1_routes.api_router)

@app.get("/")
def read_root():
    return {"message": "NutriBox API está funcionando!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
