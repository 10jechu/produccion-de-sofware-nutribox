from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.core_models import Hijo
from app.schemas.hijo import HijoCreate, HijoUpdate, HijoRead

router = APIRouter(prefix="/api/v1/hijos", tags=["04 - Hijos"])

@router.post("/", response_model=HijoRead, status_code=status.HTTP_201_CREATED)
def crear_hijo(payload: HijoCreate, db: Session = Depends(get_db)):
    obj = Hijo(**payload.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=list[HijoRead])
def listar_hijos(db: Session = Depends(get_db)):
    return db.query(Hijo).all()

@router.get("/{id}", response_model=HijoRead)
def obtener_hijo(id: int, db: Session = Depends(get_db)):
    obj = db.get(Hijo, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Hijo no encontrado")
    return obj

@router.patch("/{id}", response_model=HijoRead)
def actualizar_hijo(id: int, payload: HijoUpdate, db: Session = Depends(get_db)):
    obj = db.get(Hijo, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Hijo no encontrado")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_hijo(id: int, db: Session = Depends(get_db)):
    obj = db.get(Hijo, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Hijo no encontrado")
    db.delete(obj)
    db.commit()
