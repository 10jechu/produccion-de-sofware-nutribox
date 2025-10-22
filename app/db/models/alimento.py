from typing import List, Optional
from sqlmodel import Relationship
from typing import List
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.orm import relationship

class Alimento(SQLModel, table=True):
    __tablename__ = "alimentos"
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    calorias: int
    loncheras: List["LoncheraAlimento"] = Relationship(back_populates="alimento", sa_relationship_kwargs={"cascade":"all, delete-orphan"})