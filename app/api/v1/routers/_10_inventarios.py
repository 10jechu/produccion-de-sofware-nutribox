from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from app.db.session import engine
from app.db.models.inventario import Inventario

router = APIRouter(prefix="/api/v1/inventarios", tags=["10 - Inventarios"])

@router.post("/", response_model=Inventario)
def create_inventario(inventario: Inventario):
    with Session(engine) as session:
        db_inventario = Inventario.from_orm(inventario)
        session.add(db_inventario)
        session.commit()
        session.refresh(db_inventario)
        return db_inventario

@router.get("/", response_model=list[Inventario])
def list_inventarios():
    with Session(engine) as session:
        return session.exec(select(Inventario)).all()

@router.get("/{id}", response_model=Inventario)
def get_inventario(id: int):
    with Session(engine) as session:
        inventario = session.get(Inventario, id)
        if not inventario:
            raise HTTPException(status_code=404, detail="Inventario no encontrado")
        return inventario

@router.delete("/{id}")
def delete_inventario(id: int):
    with Session(engine) as session:
        inventario = session.get(Inventario, id)
        if not inventario:
            raise HTTPException(status_code=404, detail="Inventario no encontrado")
        session.delete(inventario)
        session.commit()
        return {"message": "Inventario eliminado"}
