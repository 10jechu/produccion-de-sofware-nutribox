from sqlmodel import Session
from app.db.models.historial_alimento import Historial_alimento
from app.crud.base import CRUDBase

crud_historial_alimento = CRUDBase(Historial_alimento)
