# app/db/schemas/menu.py
from pydantic import BaseModel, Field
from app.db.schemas.common import ORMModel
from app.db.schemas.food import AlimentoRead # Para mostrar info del alimento

# --- Items ---
class MenuItemCreate(BaseModel):
    alimento_id: int
    cantidad: float = Field(1.0, gt=0)

class MenuItemRead(ORMModel):
    id: int
    menu_id: int
    alimento_id: int
    cantidad: float
    # Opcional: Incluir detalles del alimento para conveniencia del frontend
    alimento: AlimentoRead | None = None

# --- Menú Predeterminado ---
class MenuPredeterminadoCreate(BaseModel):
    nombre: str = Field(min_length=3, max_length=100)
    descripcion: str | None = Field(None, max_length=255)
    # Opcional: Permitir crear items junto con el menú
    items: list[MenuItemCreate] = []

class MenuPredeterminadoUpdate(BaseModel):
    nombre: str | None = Field(None, min_length=3, max_length=100)
    descripcion: str | None = Field(None, max_length=255)

class MenuPredeterminadoRead(ORMModel):
    id: int
    nombre: str
    descripcion: str | None
    items: list[MenuItemRead] = [] # Incluir items al leer el menú

# Schema para el detalle completo al listar (incluye nutrición calculada)
class MenuPredeterminadoDetail(MenuPredeterminadoRead):
     nutricion_total: dict | None = None # Calculado en el CRUD
     costo_total: float | None = None # Calculado en el CRUD