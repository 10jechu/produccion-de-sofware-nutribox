from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class Direccion(Base):
    __tablename__ = "direcciones"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id", ondelete="CASCADE"), index=True, nullable=False)
    etiqueta: Mapped[str] = mapped_column(String(50), default="Casa")
    direccion: Mapped[str] = mapped_column(String(200), nullable=False)
    barrio: Mapped[str] = mapped_column(String(120), default="")
    ciudad: Mapped[str] = mapped_column(String(120), default="Bogotá")
    
    # Relación
    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="direcciones")
