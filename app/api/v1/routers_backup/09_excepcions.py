from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.database import engine
from app.db.models.excepcion import Excepcion
from app.crud.excepcion import crud_excepcion

router = APIRouter(prefix="/excepcions", tags=["09 - Excepciones"])

def get_session():
    with Session(engine) as session:
        yield session

@router.get("/", response_model=list[Excepcion])
def listar(session: Session = Depends(get_session)):
    return crud_excepcion.get_all(session)

@router.get("/{id}", response_model=Excepcion)
def obtener(id: int, session: Session = Depends(get_session)):
    obj = crud_excepcion.get(session, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Excepcion no encontrado")
    return obj

@router.post("/", response_model=Excepcion)
def crear(obj: Excepcion, session: Session = Depends(get_session)):
    return crud_excepcion.create(session, obj)

@router.delete("/{id}")
def eliminar(id: int, session: Session = Depends(get_session)):
    eliminado = crud_excepcion.delete(session, id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Excepcion no encontrado")
    return {"message": "Excepcion eliminado correctamente"}
