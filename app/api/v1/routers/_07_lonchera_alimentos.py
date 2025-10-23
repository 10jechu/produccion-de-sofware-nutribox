from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.lonchera_alimento import LoncheraAlimento
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/lonchera-alimentos", tags=["07 - Lonchera-Alimentos"])

class ItemCreate(BaseModel):
    lonchera_id: int
    alimento_id: int
    cantidad: float = 1.0

class ItemRead(BaseModel):
    id: int
    lonchera_id: int
    alimento_id: int
    cantidad: float
    class Config:
        from_attributes = True

@router.post("/", response_model=ItemRead, status_code=201)
def agregar_alimento_a_lonchera(payload: ItemCreate, db: Session = Depends(get_db)):
    obj = LoncheraAlimento(**payload.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/lonchera/{lonchera_id}", response_model=list[ItemRead])
def listar_alimentos_de_lonchera(lonchera_id: int, db: Session = Depends(get_db)):
    return db.query(LoncheraAlimento).filter_by(lonchera_id=lonchera_id).all()

@router.delete("/{id}", status_code=204)
def quitar_alimento_de_lonchera(id: int, db: Session = Depends(get_db)):
    obj = db.get(LoncheraAlimento, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    db.delete(obj)
    db.commit()
