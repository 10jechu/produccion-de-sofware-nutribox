from sqlmodel import SQLModel, Field

class HijoRestriccionLink(SQLModel, table=True):
    __tablename__ = "hijos_restricciones"
    hijo_id: int = Field(foreign_key="hijos.id", primary_key=True)
    restriccion_id: int = Field(foreign_key="restriccion.id", primary_key=True)
