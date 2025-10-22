from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class LoncheraAlimento(SQLModel, table=True):
    __tablename__ = "lonchera_alimentos"

    id: Optional[int] = Field(default=None, primary_key=True)
    lonchera_id: int = Field(foreign_key="loncheras.id", index=True)
    alimento_id: int = Field(foreign_key="alimentos.id", index=True)
    cantidad: int = Field(default=0)

    lonchera: "Lonchera" = Relationship(back_populates="alimentos")
    alimento: "Alimento" = Relationship(back_populates="loncheras")
