from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base_class import Base

class Direccion(Base):
    __tablename__ = "direcciones"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    etiqueta = Column(String(50), default="Casa")
    direccion = Column(String(200), nullable=False)
    barrio = Column(String(120), default="")
    ciudad = Column(String(120), default="Bogotá")
