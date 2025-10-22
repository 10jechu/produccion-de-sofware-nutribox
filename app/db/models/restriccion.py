from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class Restriccion(Base):
    __tablename__ = "restricciones"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    hijo_id: Mapped[int] = mapped_column(ForeignKey("hijos.id", ondelete="CASCADE"), index=True, nullable=False)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)  # 'alergia' o 'prohibido'
    alimento_id: Mapped[int | None] = mapped_column(ForeignKey("alimentos.id"), index=True, nullable=True)  # Para tipo='alergia'
    texto: Mapped[str | None] = mapped_column(String(255), nullable=True)  # Para tipo='prohibido'
    
    # Relaciones
    hijo: Mapped["Hijo"] = relationship("Hijo", back_populates="restricciones")
    alimento: Mapped["Alimento"] = relationship("Alimento")
