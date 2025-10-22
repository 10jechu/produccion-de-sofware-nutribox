from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from app.db.session import engine
from app.db.models.excepcion import Excepcion

router = APIRouter(prefix="/api/v1/excepcions", tags=["09 - Excepciones"])

@router.post("/", response_model=Excepcion)
def create_excepcion(excepcion: Excepcion):
    with Session(engine) as session:
        db_excepcion = Excepcion.from_orm(excepcion)
        session.add(db_excepcion)
        session.commit()
        session.refresh(db_excepcion)
        return db_excepcion

@router.get("/", response_model=list[Excepcion])
def list_excepcions():
    with Session(engine) as session:
        return session.exec(select(Excepcion)).all()

@router.get("/{id}", response_model=Excepcion)
def get_excepcion(id: int):
    with Session(engine) as session:
        excepcion = session.get(Excepcion, id)
        if not excepcion:
            raise HTTPException(status_code=404, detail="Excepcion no encontrada")
        return excepcion

@router.delete("/{id}")
def delete_excepcion(id: int):
    with Session(engine) as session:
        excepcion = session.get(Excepcion, id)
        if not excepcion:
            raise HTTPException(status_code=404, detail="Excepcion no encontrada")
        session.delete(excepcion)
        session.commit()
        return {"message": "Excepcion eliminada"}
