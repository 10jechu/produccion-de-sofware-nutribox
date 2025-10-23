from sqlmodel import Session
from app.db.models.lonchera_alimento import Lonchera_alimento
from app.crud.base import CRUDBase

crud_lonchera_alimento = CRUDBase(Lonchera_alimento)
