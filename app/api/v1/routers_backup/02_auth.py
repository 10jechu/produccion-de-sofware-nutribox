from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["02 - Autenticación"])

@router.get("/")
def get_auth():
    return {"msg": "Obtener autenticación"}

@router.post("/")
def create_auth():
    return {"msg": "Crear autenticación"}
