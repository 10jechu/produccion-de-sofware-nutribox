from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from .hijo import Hijo
from sqlalchemy.orm import relationship

class Restriccion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tipo: str
    hijo_id: Optional[int] = Field(foreign_key="hijo.id")
    hijo: Optional[Hijo] = Relationship(back_populates="restriccions")
    excepcions: List["Excepcion"] = Relationship(back_populates="restriccion")