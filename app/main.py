from fastapi import FastAPI
from app.api.v1.routes import api_router
from app.db.session import init_db

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/health")
def health():
    return {"status":"ok"}

app.include_router(api_router)
