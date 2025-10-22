from typing import Optional
from sqlmodel import SQLModel, Field
from .hijo import Hijo

class Restriccion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tipo: str
    hijo_id: Optional[int] = Field(foreign_key="hijo.id")
    hijo: Optional[Hijo] = Relationship(back_populates="restriccions")
