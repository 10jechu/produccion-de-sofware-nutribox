from sqlmodel import SQLModel, Field

class LoncheraAlimento(SQLModel, table=True):
    __tablename__ = "lonchera_alimento"
    lonchera_id: int = Field(foreign_key="lonchera.id", primary_key=True)
    alimento_id: int = Field(foreign_key="alimento.id", primary_key=True)
