from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.database import engine
from app.db.models.lonchera import Lonchera
from app.crud.lonchera import crud_lonchera

router = APIRouter(prefix="/loncheras", tags=["05 - Loncheras"])

def get_session():
    with Session(engine) as session:
        yield session

@router.get("/", response_model=list[Lonchera])
def listar(session: Session = Depends(get_session)):
    return crud_lonchera.get_all(session)

@router.get("/{id}", response_model=Lonchera)
def obtener(id: int, session: Session = Depends(get_session)):
    obj = crud_lonchera.get(session, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Lonchera no encontrado")
    return obj

@router.post("/", response_model=Lonchera)
def crear(obj: Lonchera, session: Session = Depends(get_session)):
    return crud_lonchera.create(session, obj)

@router.delete("/{id}")
def eliminar(id: int, session: Session = Depends(get_session)):
    eliminado = crud_lonchera.delete(session, id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Lonchera no encontrado")
    return {"message": "Lonchera eliminado correctamente"}
