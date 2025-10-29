from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.db.schemas.lunchbox import LoncheraRead
from app.crud import lunchbox as crud

router = APIRouter(prefix="/menus", tags=["menus"])

# Endpoint que lista las loncheras creadas por el Admin (ID 1) como 'menús'
@router.get('/', response_model=list[LoncheraRead], summary='Listar Menus Predeterminados')
def list_menus(db: Session = Depends(get_db)):
    # SIMULACIÓN: Filtraremos por el ID del usuario Admin de prueba (ID 1)
    return crud.list_(db, usuario_id=1)
