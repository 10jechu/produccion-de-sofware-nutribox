from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.database import engine
from app.db.models.restriccion import Restriccion
from app.crud.restriccion import crud_restriccion

router = APIRouter(prefix="/restriccions", tags=["08 - Restricciones"])

def get_session():
    with Session(engine) as session:
        yield session

@router.get("/", response_model=list[Restriccion])
def listar(session: Session = Depends(get_session)):
    return crud_restriccion.get_all(session)

@router.get("/{id}", response_model=Restriccion)
def obtener(id: int, session: Session = Depends(get_session)):
    obj = crud_restriccion.get(session, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Restriccion no encontrado")
    return obj

@router.post("/", response_model=Restriccion)
def crear(obj: Restriccion, session: Session = Depends(get_session)):
    return crud_restriccion.create(session, obj)

@router.delete("/{id}")
def eliminar(id: int, session: Session = Depends(get_session)):
    eliminado = crud_restriccion.delete(session, id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Restriccion no encontrado")
    return {"message": "Restriccion eliminado correctamente"}
