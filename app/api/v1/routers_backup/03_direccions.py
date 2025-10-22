from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.database import engine
from app.db.models.direccion import Direccion
from app.crud.direccion import crud_direccion

router = APIRouter(prefix="/direccions", tags=["03 - Direcciones"])

def get_session():
    with Session(engine) as session:
        yield session

@router.get("/", response_model=list[Direccion])
def listar(session: Session = Depends(get_session)):
    return crud_direccion.get_all(session)

@router.get("/{id}", response_model=Direccion)
def obtener(id: int, session: Session = Depends(get_session)):
    obj = crud_direccion.get(session, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Direccion no encontrado")
    return obj

@router.post("/", response_model=Direccion)
def crear(obj: Direccion, session: Session = Depends(get_session)):
    return crud_direccion.create(session, obj)

@router.delete("/{id}")
def eliminar(id: int, session: Session = Depends(get_session)):
    eliminado = crud_direccion.delete(session, id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Direccion no encontrado")
    return {"message": "Direccion eliminado correctamente"}
