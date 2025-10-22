from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.database import engine
from app.db.models.alimento import Alimento
from app.crud.alimento import crud_alimento

router = APIRouter(prefix="/alimentos", tags=["06 - Alimentos"])

def get_session():
    with Session(engine) as session:
        yield session

@router.get("/", response_model=list[Alimento])
def listar(session: Session = Depends(get_session)):
    return crud_alimento.get_all(session)

@router.get("/{id}", response_model=Alimento)
def obtener(id: int, session: Session = Depends(get_session)):
    obj = crud_alimento.get(session, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")
    return obj

@router.post("/", response_model=Alimento)
def crear(obj: Alimento, session: Session = Depends(get_session)):
    return crud_alimento.create(session, obj)

@router.delete("/{id}")
def eliminar(id: int, session: Session = Depends(get_session)):
    eliminado = crud_alimento.delete(session, id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")
    return {"message": "Alimento eliminado correctamente"}
