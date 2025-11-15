from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from app.db.schemas.common import ORMModel

class MenuItemCreate(BaseModel):
    alimento_id: int
    cantidad: int = 1

class MenuCreate(BaseModel):
    nombre: str
    descripcion: str = ""
    dia_semana: str  # "Lunes", "Martes", etc.
    alimentos: List[MenuItemCreate] = []

class MenuUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    dia_semana: Optional[str] = None
    activo: Optional[bool] = None

class MenuItemRead(ORMModel):
    alimento_id: int
    nombre: str
    cantidad: int
    kcal: float
    proteinas: float
    carbos: float

class MenuRead(ORMModel):
    id: int
    nombre: str
    descripcion: str
    dia_semana: str
    activo: bool
    usuario_id: int
    alimentos: List[MenuItemRead] = []

class MenuDetail(ORMModel):
    id: int
    nombre: str
    descripcion: str
    dia_semana: str
    activo: bool
    usuario_id: int
    creador_nombre: str
    alimentos: List[MenuItemRead] = []
    nutricion_total: dict = {}
