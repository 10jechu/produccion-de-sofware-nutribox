from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from app.db.session import get_session
from app.db.models.direccion import Direccion

router = APIRouter(prefix="/api/v1/direccions", tags=["03 - Direcciones"])

@router.post("/", response_model=Direccion)
def create_direccion(direccion: Direccion):
    with Session(engine) as session:
        db_direccion = Direccion.from_orm(direccion)
        session.add(db_direccion)
        session.commit()
        session.refresh(db_direccion)
        return db_direccion

@router.get("/", response_model=list[Direccion])
def list_direccions():
    with Session(engine) as session:
        return session.exec(select(Direccion)).all()

@router.get("/{id}", response_model=Direccion)
def get_direccion(id: int):
    with Session(engine) as session:
        direccion = session.get(Direccion, id)
        if not direccion:
            raise HTTPException(status_code=404, detail="Direccion no encontrada")
        return direccion

@router.delete("/{id}")
def delete_direccion(id: int):
    with Session(engine) as session:
        direccion = session.get(Direccion, id)
        if not direccion:
            raise HTTPException(status_code=404, detail="Direccion no encontrada")
        session.delete(direccion)
        session.commit()
        return {"message": "Direccion eliminada"}
