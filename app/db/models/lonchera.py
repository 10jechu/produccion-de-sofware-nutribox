from sqlalchemy import Integer, String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from app.db.base_class import Base

class Lonchera(Base):
    __tablename__ = "loncheras"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    hijo_id: Mapped[int] = mapped_column(ForeignKey("hijos.id", ondelete="CASCADE"), index=True, nullable=False)
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    estado: Mapped[str] = mapped_column(String(20), default="Borrador", nullable=False)  # Borrador, Asignada, Confirmada, Archivada
    direccion_id: Mapped[int | None] = mapped_column(ForeignKey("direcciones.id"), index=True, nullable=True)
    
    # Relaciones
    hijo: Mapped["Hijo"] = relationship("Hijo", back_populates="loncheras")
    direccion: Mapped["Direccion"] = relationship("Direccion")
    items: Mapped[list["LoncheraAlimento"]] = relationship("LoncheraAlimento", back_populates="lonchera", cascade="all, delete-orphan")
