from sqlalchemy import Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.database import Base

class HistorialAlimento(Base):
    __tablename__ = "historial_alimentos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    alimento_id: Mapped[int] = mapped_column(ForeignKey("alimentos.id"), nullable=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    accion: Mapped[str] = mapped_column(String(50))  # 'eliminado', 'restaurado'
    fecha: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    motivo: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Relaciones
    alimento = relationship("Alimento")
    usuario = relationship("Usuario")
