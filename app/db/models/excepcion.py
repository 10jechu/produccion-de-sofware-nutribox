from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class Excepcion(SQLModel, table=True):
    __tablename__ = "excepcion"
    id: Optional[int] = Field(default=None, primary_key=True)
    descripcion: str = ""
    hijo_id: int = Field(foreign_key="hijos.id", index=True)

    hijo: "Hijo" = Relationship()
