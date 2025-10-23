from sqlmodel import Session
from app.db.models.alimento import Alimento
from app.crud.base import CRUDBase

crud_alimento = CRUDBase(Alimento)
