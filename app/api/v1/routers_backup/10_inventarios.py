from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.database import engine
from app.db.models.inventario import Inventario
from app.crud.inventario import crud_inventario

router = APIRouter(prefix="/inventarios", tags=["10 - Inventario"])

def get_session():
    with Session(engine) as session:
        yield session

@router.get("/", response_model=list[Inventario])
def listar(session: Session = Depends(get_session)):
    return crud_inventario.get_all(session)

@router.get("/{id}", response_model=Inventario)
def obtener(id: int, session: Session = Depends(get_session)):
    obj = crud_inventario.get(session, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    return obj

@router.post("/", response_model=Inventario)
def crear(obj: Inventario, session: Session = Depends(get_session)):
    return crud_inventario.create(session, obj)

@router.delete("/{id}")
def eliminar(id: int, session: Session = Depends(get_session)):
    eliminado = crud_inventario.delete(session, id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    return {"message": "Inventario eliminado correctamente"}
