from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Alimento(Base):
    __tablename__ = "alimentos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(120), unique=True, nullable=False)
    calorias = Column(Integer, nullable=False, default=0)
    proteinas = Column(Float, default=0.0)
    carbohidratos = Column(Float, default=0.0)
    unidad = Column(String(20), default="g")
    activo = Column(Boolean, default=True)
    
    lonchera_items = relationship("LoncheraAlimento", back_populates="alimento", cascade="all, delete-orphan")
