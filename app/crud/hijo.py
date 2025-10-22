from sqlmodel import Session
from app.db.models.hijo import Hijo
from app.crud.base import CRUDBase

crud_hijo = CRUDBase(Hijo)
