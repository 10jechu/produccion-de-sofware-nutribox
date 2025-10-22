from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Integer, ForeignKey

class LoncheraAlimento(SQLModel, table=True):
    __tablename__ = "lonchera_alimentos"

    id: Optional[int] = Field(default=None, primary_key=True)
    lonchera_id: int = Field(sa_column=Column(Integer, ForeignKey("loncheras.id", ondelete="CASCADE"), nullable=False, index=True))
    alimento_id: int = Field(sa_column=Column(Integer, ForeignKey("alimentos.id", ondelete="CASCADE"), nullable=False, index=True))
    cantidad: int

    lonchera: "Lonchera" = Relationship(back_populates="items")
    alimento: "Alimento" = Relationship(back_populates="loncheras")
