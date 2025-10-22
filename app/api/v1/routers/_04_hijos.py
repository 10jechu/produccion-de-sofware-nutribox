from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.db.session import get_session
from app.db.models.hijo import Hijo
from app.schemas import HijoCreate, HijoUpdate, HijoRead

router = APIRouter(prefix="/api/v1/hijos", tags=["hijos"])

@router.post("/", response_model=HijoRead, status_code=status.HTTP_201_CREATED)
def crear_hijo(payload: HijoCreate, db: Session = Depends(get_session)):
    try:
        obj = Hijo(
            nombre=payload.nombre,
            fecha_nacimiento=payload.fecha_nacimiento,
            usuario_id=payload.usuario_id,
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {getattr(e, 'orig', e)}")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"SQLAlchemyError: {e.__class__.__name__}: {e}")

@router.get("/", response_model=list[HijoRead])
def listar_hijos(db: Session = Depends(get_session)):
    return db.query(Hijo).all()

@router.get("/{id}", response_model=HijoRead)
def obtener_hijo(id: int, db: Session = Depends(get_session)):
    obj = db.get(Hijo, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Hijo no encontrado")
    return obj

@router.patch("/{id}", response_model=HijoRead)
def actualizar_hijo(id: int, payload: HijoUpdate, db: Session = Depends(get_session)):
    obj = db.get(Hijo, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Hijo no encontrado")

    data = payload.dict(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, v)

    try:
        db.commit()
        db.refresh(obj)
        return obj
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {getattr(e, 'orig', e)}")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_hijo(id: int, db: Session = Depends(get_session)):
    obj = db.get(Hijo, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Hijo no encontrado")
    db.delete(obj)
    db.commit()
    return None
