from sqlmodel import Session
from app.db.models.restriccion import Restriccion
from app.crud.base import CRUDBase

crud_restriccion = CRUDBase(Restriccion)
