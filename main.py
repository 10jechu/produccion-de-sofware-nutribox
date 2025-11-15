from fastapi import FastAPI
from app.api.v1.routers import routes as api_v1_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="NutriBox API",
    description="API para la plataforma NutriBox - Gestión de loncheras escolares",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir todos los routers de la API v1
app.include_router(api_v1_routes.api_router)

@app.get("/")
def read_root():
    return {"message": "NutriBox API está funcionando!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
