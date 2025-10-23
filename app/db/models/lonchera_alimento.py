from sqlalchemy import Column, Integer, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class LoncheraAlimento(Base):
    __tablename__ = "lonchera_alimento"
    id = Column(Integer, primary_key=True, index=True)
    lonchera_id = Column(Integer, ForeignKey("loncheras.id", ondelete="CASCADE"), nullable=False, index=True)
    alimento_id = Column(Integer, ForeignKey("alimentos.id", ondelete="CASCADE"), nullable=False, index=True)
    cantidad = Column(Float, nullable=False, default=1.0)
    
    lonchera = relationship("Lonchera", back_populates="items")
    alimento = relationship("Alimento", back_populates="lonchera_items")
    
    __table_args__ = (UniqueConstraint("lonchera_id", "alimento_id", name="uq_lonchera_alimento"),)
