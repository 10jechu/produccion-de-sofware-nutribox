from sqlmodel import Session
from app.db.models.excepcion import Excepcion
from app.crud.base import CRUDBase

crud_excepcion = CRUDBase(Excepcion)
