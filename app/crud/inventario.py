from sqlmodel import Session
from app.db.models.inventario import Inventario
from app.crud.base import CRUDBase

crud_inventario = CRUDBase(Inventario)
