from sqlmodel import SQLModel, Field

class LoncheraAlimentoLink(SQLModel, table=True):
    __tablename__ = "lonchera_alimentos"
    lonchera_id: int = Field(foreign_key="lonchera.id", primary_key=True)
    alimento_id: int = Field(foreign_key="alimento.id", primary_key=True)
    # Si quieres guardar cantidad u otros campos, agrega aquí:
    # cantidad: int | None = None
