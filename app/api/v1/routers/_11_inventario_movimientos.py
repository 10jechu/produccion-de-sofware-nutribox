from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from app.db.session import engine
from app.db.models.inventario_movimiento import Inventario_Movimiento

router = APIRouter(prefix="/api/v1/inventario_movimientos", tags=["11 - Inventario_Movimientos"])

@router.post("/", response_model=Inventario_Movimiento)
def create_inventario_movimiento(inventario_movimiento: Inventario_Movimiento):
    with Session(engine) as session:
        db_inventario_movimiento = Inventario_Movimiento.from_orm(inventario_movimiento)
        session.add(db_inventario_movimiento)
        session.commit()
        session.refresh(db_inventario_movimiento)
        return db_inventario_movimiento

@router.get("/", response_model=list[Inventario_Movimiento])
def list_inventario_movimientos():
    with Session(engine) as session:
        return session.exec(select(Inventario_Movimiento)).all()

@router.get("/{id}", response_model=Inventario_Movimiento)
def get_inventario_movimiento(id: int):
    with Session(engine) as session:
        inventario_movimiento = session.get(Inventario_Movimiento, id)
        if not inventario_movimiento:
            raise HTTPException(status_code=404, detail="Inventario_Movimiento no encontrado")
        return inventario_movimiento

@router.delete("/{id}")
def delete_inventario_movimiento(id: int):
    with Session(engine) as session:
        inventario_movimiento = session.get(Inventario_Movimiento, id)
        if not inventario_movimiento:
            raise HTTPException(status_code=404, detail="Inventario_Movimiento no encontrado")
        session.delete(inventario_movimiento)
        session.commit()
        return {"message": "Inventario_Movimiento eliminado"}
