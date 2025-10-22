from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from typing import List
from sqlmodel import Relationship
from datetime import date
from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Lonchera(Base):
        __tablename__ = "loncheras"
__tablename__ = "lonchera"

    id = Column(Integer, primary_key=True, index=True)
    hijo_id = Column(Integer, ForeignKey("hijo.id"), index=True, nullable=False)
    fecha = Column(Date, nullable=False)
    hijo: "Hijo" = Relationship(back_populates="loncheras")
    hijo: "Hijo" = Relationship(back_populates="loncheras")
    items = relationship('Lonchera_Alimento', back_populates='lonchera', cascade='all, delete-orphan')