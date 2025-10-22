from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from app.db.session import get_session
from app.db.models.historial_alimento import Historial_Alimento

router = APIRouter(prefix="/api/v1/historial_alimentos", tags=["12 - Historial_Alimentos"])

@router.post("/", response_model=Historial_Alimento)
def create_historial_alimento(historial_alimento: Historial_Alimento):
    with Session(engine) as session:
        db_historial_alimento = Historial_Alimento.from_orm(historial_alimento)
        session.add(db_historial_alimento)
        session.commit()
        session.refresh(db_historial_alimento)
        return db_historial_alimento

@router.get("/", response_model=list[Historial_Alimento])
def list_historial_alimentos():
    with Session(engine) as session:
        return session.exec(select(Historial_Alimento)).all()

@router.get("/{id}", response_model=Historial_Alimento)
def get_historial_alimento(id: int):
    with Session(engine) as session:
        historial_alimento = session.get(Historial_Alimento, id)
        if not historial_alimento:
            raise HTTPException(status_code=404, detail="Historial_Alimento no encontrado")
        return historial_alimento

@router.delete("/{id}")
def delete_historial_alimento(id: int):
    with Session(engine) as session:
        historial_alimento = session.get(Historial_Alimento, id)
        if not historial_alimento:
            raise HTTPException(status_code=404, detail="Historial_Alimento no encontrado")
        session.delete(historial_alimento)
        session.commit()
        return {"message": "Historial_Alimento eliminado"}
