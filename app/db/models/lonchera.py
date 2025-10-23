from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Lonchera(Base):
    __tablename__ = "loncheras"
    id = Column(Integer, primary_key=True, index=True)
    hijo_id = Column(Integer, ForeignKey("hijos.id", ondelete="CASCADE"), nullable=False, index=True)
    fecha = Column(Date, nullable=False)
    estado = Column(String(20), default="Borrador")
    direccion_id = Column(Integer, ForeignKey("direcciones.id"), nullable=True, index=True)
    
    hijo = relationship("Hijo", back_populates="loncheras")
    direccion = relationship("Direccion")
    items = relationship("LoncheraAlimento", back_populates="lonchera", cascade="all, delete-orphan")
