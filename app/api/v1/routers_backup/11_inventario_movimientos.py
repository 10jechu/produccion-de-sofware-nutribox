from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.database import engine
from app.db.models.inventario_movimiento import InventarioMovimiento
from app.crud.base import CRUDBase

crud_inventario_movimiento = CRUDBase(InventarioMovimiento)
router = APIRouter(prefix="/inventario_movimientos", tags=["11 - Movimientos de Inventario"])

def get_session():
    with Session(engine) as session:
        yield session

@router.get("/", response_model=list[InventarioMovimiento])
def listar(session: Session = Depends(get_session)):
    return crud_inventario_movimiento.get_all(session)

@router.get("/{id}", response_model=InventarioMovimiento)
def obtener(id: int, session: Session = Depends(get_session)):
    obj = crud_inventario_movimiento.get(session, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    return obj

@router.post("/", response_model=InventarioMovimiento)
def crear(obj: InventarioMovimiento, session: Session = Depends(get_session)):
    return crud_inventario_movimiento.create(session, obj)

@router.delete("/{id}")
def eliminar(id: int, session: Session = Depends(get_session)):
    eliminado = crud_inventario_movimiento.delete(session, id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    return {"message": "Movimiento eliminado correctamente"}
