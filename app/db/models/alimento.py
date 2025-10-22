from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Alimento(SQLModel, table=True):
    __tablename__ = "alimentos"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    calorias: int
    unidad: str

    loncheras: List["LoncheraAlimento"] = Relationship(back_populates="alimento", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
