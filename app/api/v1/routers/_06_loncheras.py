from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.lonchera import Lonchera
from app.schemas.lonchera import LoncheraCreate, LoncheraUpdate, LoncheraRead

router = APIRouter(prefix="/api/v1/loncheras", tags=["06 - Loncheras"])

@router.post("/", response_model=LoncheraRead, status_code=status.HTTP_201_CREATED)
def crear_lonchera(payload: LoncheraCreate, db: Session = Depends(get_db)):
    obj = Lonchera(**payload.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=list[LoncheraRead])
def listar_loncheras(db: Session = Depends(get_db)):
    return db.query(Lonchera).all()

@router.get("/{id}", response_model=LoncheraRead)
def obtener_lonchera(id: int, db: Session = Depends(get_db)):
    obj = db.get(Lonchera, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Lonchera no encontrada")
    return obj

@router.patch("/{id}", response_model=LoncheraRead)
def actualizar_lonchera(id: int, payload: LoncheraUpdate, db: Session = Depends(get_db)):
    obj = db.get(Lonchera, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Lonchera no encontrada")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_lonchera(id: int, db: Session = Depends(get_db)):
    obj = db.get(Lonchera, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Lonchera no encontrada")
    db.delete(obj)
    db.commit()
