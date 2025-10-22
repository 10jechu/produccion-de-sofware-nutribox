from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field, Relationship

class Historial_Alimento(SQLModel, table=True):
    __tablename__ = "historial_alimento"
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha: date
    estado: str = ""
    hijo_id: int = Field(foreign_key="hijos.id", index=True)
    alimento_id: int = Field(foreign_key="alimento.id", index=True)

    hijo: "Hijo" = Relationship()
    alimento: "Alimento" = Relationship()
