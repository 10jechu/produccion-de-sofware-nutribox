from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.database import engine
from app.db.models.historial_alimento import HistorialAlimento
from app.crud.base import CRUDBase

crud_historial_alimento = CRUDBase(HistorialAlimento)
router = APIRouter(prefix="/historial_alimentos", tags=["12 - Historial"])

def get_session():
    with Session(engine) as session:
        yield session

@router.get("/", response_model=list[HistorialAlimento])
def listar(session: Session = Depends(get_session)):
    return crud_historial_alimento.get_all(session)

@router.get("/{id}", response_model=HistorialAlimento)
def obtener(id: int, session: Session = Depends(get_session)):
    obj = crud_historial_alimento.get(session, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    return obj

@router.post("/", response_model=HistorialAlimento)
def crear(obj: HistorialAlimento, session: Session = Depends(get_session)):
    return crud_historial_alimento.create(session, obj)

@router.delete("/{id}")
def eliminar(id: int, session: Session = Depends(get_session)):
    eliminado = crud_historial_alimento.delete(session, id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    return {"message": "Historial eliminado correctamente"}
