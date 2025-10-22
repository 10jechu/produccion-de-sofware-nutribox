from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from .usuario import Usuario

class Hijo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    padre_id: Optional[int] = Field(foreign_key="usuario.id")
    padre: Optional[Usuario] = Relationship(back_populates="hijos")
