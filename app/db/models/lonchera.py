from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Lonchera(Base):
    __tablename__ = "loncheras"
    
    id = Column(Integer, primary_key=True, index=True)
    hijo_id = Column(Integer, ForeignKey("hijos.id"), nullable=False, index=True)
    fecha = Column(Date, nullable=False)
    estado = Column(String(20), default="Borrador")  # Borrador, Confirmada, Archivada
    direccion_id = Column(Integer, ForeignKey("direcciones.id"), nullable=True)
    
    # Relationships
    hijo = relationship("Hijo", back_populates="loncheras")
    direccion = relationship("Direccion")
    items = relationship("LoncheraAlimento", back_populates="lonchera", cascade="all, delete-orphan")

class LoncheraAlimento(Base):
    __tablename__ = "lonchera_alimento"
    
    id = Column(Integer, primary_key=True, index=True)
    lonchera_id = Column(Integer, ForeignKey("loncheras.id"), nullable=False, index=True)
    alimento_id = Column(Integer, ForeignKey("alimentos.id"), nullable=False, index=True)
    cantidad = Column(Integer, default=1)
    
    # Relationships
    lonchera = relationship("Lonchera", back_populates="items")
    alimento = relationship("Alimento", back_populates="lonchera_items")
