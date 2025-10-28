from pydantic import BaseModel
from datetime import date

class RolMini(BaseModel):
    id: int
    nombre: str

class MembresiaMini(BaseModel):
    id: int
    tipo: str
    max_direcciones: int

class HijoMini(BaseModel):
    id: int
    nombre: str
    restricciones_count: int = 0
    loncheras_activas: int = 0

class DireccionMini(BaseModel):
    id: int
    etiqueta: str
    direccion: str
    ciudad: str

class ResumenUsuario(BaseModel):
    total_hijos: int
    total_direcciones: int
    total_loncheras: int
    loncheras_este_mes: int

class UserDetail(BaseModel):
    id: int
    nombre: str
    email: str
    rol: RolMini
    membresia: MembresiaMini
    hijos: list[HijoMini]
    direcciones: list[DireccionMini]
    resumen: ResumenUsuario

class RestriccionMini(BaseModel):
    id: int
    tipo: str
    alimento_nombre: str | None = None
    texto: str | None = None

class LoncheraMini(BaseModel):
    id: int
    fecha: date
    estado: str
    items_count: int

class PadreMini(BaseModel):
    id: int
    nombre: str

class EstadisticasHijo(BaseModel):
    total_loncheras: int
    promedio_calorias: float

class ChildDetail(BaseModel):
    id: int
    nombre: str
    usuario_id: int
    padre: PadreMini
    restricciones: list[RestriccionMini]
    loncheras_recientes: list[LoncheraMini]
    estadisticas: EstadisticasHijo

class NutricionTotal(BaseModel):
    calorias: float
    proteinas: float
    carbohidratos: float
    costo_total: float # NUEVO CAMPO: COSTO TOTAL

class ItemNutricional(BaseModel):
    alimento_id: int
    nombre: str
    cantidad: float
    kcal: float
    proteinas: float
    carbos: float
    costo: float # NUEVO CAMPO: COSTO POR UNIDAD

class LunchboxDetailFull(BaseModel):
    id: int
    hijo: HijoMini
    fecha: date
    estado: str
    items: list[ItemNutricional]
    direccion: DireccionMini | None
    nutricion_total: NutricionTotal
    alertas: list[str] = []
