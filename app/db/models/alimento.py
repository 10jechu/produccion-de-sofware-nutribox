from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Alimento(Base):
    __tablename__ = "alimentos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(120), unique=True, nullable=False, index=True)
    descripcion = Column(String(255), nullable=True)
    calorias = Column(Float, nullable=False, default=0.0)
    proteinas = Column(Float, nullable=False, default=0.0)
    grasas = Column(Float, nullable=False, default=0.0)
    carbohidratos = Column(Float, nullable=False, default=0.0)
    activo = Column(Boolean, default=True)
    
    # Relationships
    lonchera_items = relationship("LoncheraAlimento", back_populates="alimento", cascade="all, delete-orphan")
