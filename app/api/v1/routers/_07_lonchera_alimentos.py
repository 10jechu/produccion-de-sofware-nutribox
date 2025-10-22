from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from app.db.session import get_session
from app.db.models.lonchera_alimento import LoncheraAlimento

router = APIRouter(prefix="/api/v1/lonchera_alimentos", tags=["07 - Lonchera_Alimentos"])

@router.post("/", response_model=LoncheraAlimento)
def create_lonchera_alimento(lonchera_alimento: LoncheraAlimento):
    with Session(engine) as session:
        db_lonchera_alimento = LoncheraAlimento.from_orm(lonchera_alimento)
        session.add(db_lonchera_alimento)
        session.commit()
        session.refresh(db_lonchera_alimento)
        return db_lonchera_alimento

@router.get("/", response_model=list[LoncheraAlimento])
def list_lonchera_alimentos():
    with Session(engine) as session:
        return session.exec(select(LoncheraAlimento)).all()

@router.get("/{id}", response_model=LoncheraAlimento)
def get_lonchera_alimento(id: int):
    with Session(engine) as session:
        lonchera_alimento = session.get(LoncheraAlimento, id)
        if not lonchera_alimento:
            raise HTTPException(status_code=404, detail="LoncheraAlimento no encontrado")
        return lonchera_alimento

@router.delete("/{id}")
def delete_lonchera_alimento(id: int):
    with Session(engine) as session:
        lonchera_alimento = session.get(LoncheraAlimento, id)
        if not lonchera_alimento:
            raise HTTPException(status_code=404, detail="LoncheraAlimento no encontrado")
        session.delete(lonchera_alimento)
        session.commit()
        return {"message": "LoncheraAlimento eliminado"}
