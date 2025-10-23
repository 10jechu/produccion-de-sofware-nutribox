from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes import api_router
from app.db.session import init_db

app = FastAPI(
    title="NutriBox API",
    version="2.1.0",
    description="API para gestión de loncheras escolares"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok", "version": "2.1.0"}

app.include_router(api_router)
