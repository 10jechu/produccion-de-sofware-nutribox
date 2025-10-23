from sqlmodel import Session
from app.db.models.inventario_movimiento import Inventario_movimiento
from app.crud.base import CRUDBase

crud_inventario_movimiento = CRUDBase(Inventario_movimiento)
