from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Restriccion(Base):
    __tablename__ = "restricciones"
    
    id = Column(Integer, primary_key=True, index=True)
    hijo_id = Column(Integer, ForeignKey("hijos.id"), nullable=False, index=True)
    tipo = Column(String(20), nullable=False)  # 'alergia' o 'prohibido'
    alimento_id = Column(Integer, ForeignKey("alimentos.id"), nullable=True)
    texto = Column(String(200), nullable=True)
    motivo = Column(String(255), nullable=True)
    
    # Relationships
    hijo = relationship("Hijo", back_populates="restricciones")
    alimento = relationship("Alimento")
