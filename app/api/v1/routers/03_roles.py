from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_db
from app.db.models.rol import Rol
from pydantic import BaseModel, ConfigDict

router = APIRouter(prefix="/roles", tags=["03 - Roles"])

# Schema
class RolRead(BaseModel):
    id: int
    nombre: str
    model_config = ConfigDict(from_attributes=True)

# Endpoints
@router.get("/", response_model=List[RolRead], summary="Listar roles disponibles")
def list_roles(db: Session = Depends(get_db)):
    """Obtener todos los roles del sistema"""
    return db.query(Rol).all()
