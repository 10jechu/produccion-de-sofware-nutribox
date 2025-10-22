from sqlmodel import Session
from app.db.models.direccion import Direccion
from app.crud.base import CRUDBase

crud_direccion = CRUDBase(Direccion)
