from pydantic import BaseModel
from app.db.schemas.common import ORMModel

class RestriccionCreate(BaseModel):
    hijo_id: int
    tipo: str                # 'alergia' | 'prohibido'
    alimento_id: int | None = None
    texto: str | None = None

class RestriccionRead(ORMModel):
    id: int
    hijo_id: int
    tipo: str
    alimento_id: int | None = None
    texto: str | None = None
