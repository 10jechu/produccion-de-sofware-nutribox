from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import inspect

from app.db.session import get_session
from app.schemas import AlimentoCreate, AlimentoUpdate, AlimentoRead
from app.db.models.alimento import Alimento  # ajusta si tu clase está en otro módulo

router = APIRouter(prefix="/api/v1/alimentos", tags=["alimentos"])

def _cols():
    return {c.name for c in inspect(Alimento).c}

def _apply_mapping(payload_dict: dict, cols: set):
    """
    Acepta nombre|name, calorias|calories, unidad|unit y devuelve
    un dict mapeado a las columnas reales del modelo.
    """
    data = {}
    # nombre
    if "nombre" in cols and ("nombre" in payload_dict or "name" in payload_dict):
        data["nombre"] = payload_dict.get("nombre") or payload_dict.get("name")
    elif "name" in cols and ("nombre" in payload_dict or "name" in payload_dict):
        data["name"] = payload_dict.get("nombre") or payload_dict.get("name")
    # calorias
    if "calorias" in cols and ("calorias" in payload_dict or "calories" in payload_dict):
        data["calorias"] = payload_dict.get("calorias") or payload_dict.get("calories")
    elif "calories" in cols and ("calorias" in payload_dict or "calories" in payload_dict):
        data["calories"] = payload_dict.get("calorias") or payload_dict.get("calories")
    # unidad
    if "unidad" in cols and ("unidad" in payload_dict or "unit" in payload_dict):
        data["unidad"] = payload_dict.get("unidad") or payload_dict.get("unit")
    elif "unit" in cols and ("unidad" in payload_dict or "unit" in payload_dict):
        data["unit"] = payload_dict.get("unidad") or payload_dict.get("unit")
    return data

@router.post("/", response_model=AlimentoRead, status_code=status.HTTP_201_CREATED)
def crear_alimento(payload: AlimentoCreate, db: Session = Depends(get_session)):
    cols = _cols()
    data_in = payload.model_dump(by_alias=True)  # admite alias EN
    data = _apply_mapping(data_in, cols)

    try:
        obj = Alimento(**data)
        db.add(obj); db.commit(); db.refresh(obj)
        return obj
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {getattr(e, 'orig', e)}")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"SQLAlchemyError: {e.__class__.__name__}: {e}")

@router.get("/", response_model=list[AlimentoRead])
def listar_alimentos(db: Session = Depends(get_session)):
    return db.query(Alimento).all()

@router.get("/{id}", response_model=AlimentoRead)
def obtener_alimento(id: int, db: Session = Depends(get_session)):
    obj = db.get(Alimento, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")
    return obj

@router.patch("/{id}", response_model=AlimentoRead)
def actualizar_alimento(id: int, payload: AlimentoUpdate, db: Session = Depends(get_session)):
    obj = db.get(Alimento, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")

    cols = _cols()
    partial = payload.model_dump(exclude_unset=True, by_alias=True)
    changes = _apply_mapping(partial, cols)

    for k, v in changes.items():
        setattr(obj, k, v)
    try:
        db.commit(); db.refresh(obj)
        return obj
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {getattr(e, 'orig', e)}")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_alimento(id: int, db: Session = Depends(get_session)):
    obj = db.get(Alimento, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")
    db.delete(obj); db.commit()
    return None
