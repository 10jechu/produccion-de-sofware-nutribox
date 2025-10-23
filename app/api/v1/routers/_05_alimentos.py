from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.alimento import AlimentoCreate, AlimentoUpdate, AlimentoRead
from app.db.models.alimento import Alimento

router = APIRouter(prefix="/api/v1/alimentos", tags=["05 - Alimentos"])

@router.post("/", response_model=AlimentoRead, status_code=status.HTTP_201_CREATED)
def crear_alimento(payload: AlimentoCreate, db: Session = Depends(get_db)):
    obj = Alimento(**payload.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=list[AlimentoRead])
def listar_alimentos(db: Session = Depends(get_db)):
    return db.query(Alimento).all()

@router.get("/{id}", response_model=AlimentoRead)
def obtener_alimento(id: int, db: Session = Depends(get_db)):
    obj = db.get(Alimento, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")
    return obj

@router.patch("/{id}", response_model=AlimentoRead)
def actualizar_alimento(id: int, payload: AlimentoUpdate, db: Session = Depends(get_db)):
    obj = db.get(Alimento, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_alimento(id: int, db: Session = Depends(get_db)):
    obj = db.get(Alimento, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")
    db.delete(obj)
    db.commit()
