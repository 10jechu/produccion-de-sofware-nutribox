from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base_class import Base

class Restriccion(Base):
    __tablename__ = "restricciones"
    id = Column(Integer, primary_key=True, index=True)
    hijo_id = Column(Integer, ForeignKey("hijos.id", ondelete="CASCADE"), nullable=False, index=True)
    tipo = Column(String(20), nullable=False)
    alimento_id = Column(Integer, ForeignKey("alimentos.id"), nullable=True)
    texto = Column(String(100), nullable=True)
