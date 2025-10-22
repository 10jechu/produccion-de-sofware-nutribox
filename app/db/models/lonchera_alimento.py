from sqlalchemy import Integer, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class LoncheraAlimento(Base):
    __tablename__ = "lonchera_alimentos"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    lonchera_id: Mapped[int] = mapped_column(ForeignKey("loncheras.id", ondelete="CASCADE"), index=True, nullable=False)
    alimento_id: Mapped[int] = mapped_column(ForeignKey("alimentos.id", ondelete="CASCADE"), index=True, nullable=False)
    cantidad: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    
    # Relaciones
    lonchera: Mapped["Lonchera"] = relationship("Lonchera", back_populates="items")
    alimento: Mapped["Alimento"] = relationship("Alimento")
    
    # Constraint: un alimento solo puede estar una vez por lonchera
    __table_args__ = (
        UniqueConstraint("lonchera_id", "alimento_id", name="uq_lonchera_alimento"),
    )
