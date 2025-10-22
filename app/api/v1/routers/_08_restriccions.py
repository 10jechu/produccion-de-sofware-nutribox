from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from app.db.session import engine
from app.db.models.restriccion import Restriccion

router = APIRouter(prefix="/api/v1/restriccions", tags=["08 - Restricciones"])

@router.post("/", response_model=Restriccion)
def create_restriccion(restriccion: Restriccion):
    with Session(engine) as session:
        db_restriccion = Restriccion.from_orm(restriccion)
        session.add(db_restriccion)
        session.commit()
        session.refresh(db_restriccion)
        return db_restriccion

@router.get("/", response_model=list[Restriccion])
def list_restriccions():
    with Session(engine) as session:
        return session.exec(select(Restriccion)).all()

@router.get("/{id}", response_model=Restriccion)
def get_restriccion(id: int):
    with Session(engine) as session:
        restriccion = session.get(Restriccion, id)
        if not restriccion:
            raise HTTPException(status_code=404, detail="Restriccion no encontrada")
        return restriccion

@router.delete("/{id}")
def delete_restriccion(id: int):
    with Session(engine) as session:
        restriccion = session.get(Restriccion, id)
        if not restriccion:
            raise HTTPException(status_code=404, detail="Restriccion no encontrada")
        session.delete(restriccion)
        session.commit()
        return {"message": "Restriccion eliminada"}
