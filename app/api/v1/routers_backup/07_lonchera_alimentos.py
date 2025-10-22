from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.database import engine
from app.db.models.lonchera_alimento import LoncheraAlimento
from app.crud.base import CRUDBase

crud_lonchera_alimento = CRUDBase(LoncheraAlimento)
router = APIRouter(prefix="/lonchera_alimentos", tags=["07 - LoncheraAlimentos"])

def get_session():
    with Session(engine) as session:
        yield session

@router.get("/", response_model=list[LoncheraAlimento])
def listar(session: Session = Depends(get_session)):
    return crud_lonchera_alimento.get_all(session)

@router.get("/{id}", response_model=LoncheraAlimento)
def obtener(id: int, session: Session = Depends(get_session)):
    obj = crud_lonchera_alimento.get(session, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    return obj

@router.post("/", response_model=LoncheraAlimento)
def crear(obj: LoncheraAlimento, session: Session = Depends(get_session)):
    return crud_lonchera_alimento.create(session, obj)

@router.delete("/{id}")
def eliminar(id: int, session: Session = Depends(get_session)):
    eliminado = crud_lonchera_alimento.delete(session, id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    return {"message": "Relación eliminada correctamente"}
