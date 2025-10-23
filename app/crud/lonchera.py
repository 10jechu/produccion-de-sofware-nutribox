from sqlmodel import Session
from app.db.models.lonchera import Lonchera
from app.crud.base import CRUDBase

crud_lonchera = CRUDBase(Lonchera)
