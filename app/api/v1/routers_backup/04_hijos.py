from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.database import engine
from app.db.models.hijo import Hijo
from app.crud.hijo import crud_hijo

router = APIRouter(prefix="/hijos", tags=["04 - Hijos"])

def get_session():
    with Session(engine) as session:
        yield session

@router.get("/", response_model=list[Hijo])
def listar(session: Session = Depends(get_session)):
    return crud_hijo.get_all(session)

@router.get("/{id}", response_model=Hijo)
def obtener(id: int, session: Session = Depends(get_session)):
    obj = crud_hijo.get(session, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Hijo no encontrado")
    return obj

@router.post("/", response_model=Hijo)
def crear(obj: Hijo, session: Session = Depends(get_session)):
    return crud_hijo.create(session, obj)

@router.delete("/{id}")
def eliminar(id: int, session: Session = Depends(get_session)):
    eliminado = crud_hijo.delete(session, id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Hijo no encontrado")
    return {"message": "Hijo eliminado correctamente"}
