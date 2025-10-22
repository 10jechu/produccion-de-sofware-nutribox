from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from .hijo import Hijo

class Lonchera(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    descripcion: str
    hijo_id: Optional[int] = Field(foreign_key="hijo.id")
    hijo: Optional[Hijo] = Relationship(back_populates="loncheras")
    alimentos: List["Lonchera_Alimento"] = Relationship(back_populates="lonchera")
