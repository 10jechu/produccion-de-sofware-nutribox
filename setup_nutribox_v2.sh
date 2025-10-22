#!/bin/bash
set -e

echo "��� Iniciando configuración NutriBox v2 — Backend completo..."

# Crear estructura de carpetas base
mkdir -p app/core app/db/models app/api/v1/routers app/crud app/schemas scripts tests

# Crear archivos __init__.py
find app -type d -exec touch {}/__init__.py \;

# ======================================================
# CONFIGURACIÓN PRINCIPAL
# ======================================================
cat > app/core/config.py << 'PYCONF'
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "NutriBox API"
    VERSION: str = "2.1.0"
    DATABASE_URL: str = "sqlite:///./nutribox.db"
    ALLOWED_ORIGINS: list[str] = ["*"]
    SECRET_KEY: str = "dev-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24

    class Config:
        env_file = ".env"

settings = Settings()
PYCONF

# ======================================================
# CONEXIÓN A BASE DE DATOS
# ======================================================
cat > app/db/database.py << 'PYDB'
from sqlmodel import SQLModel, create_engine
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
PYDB

# ======================================================
# MODELOS BASE
# ======================================================
cat > app/db/models/role.py << 'PYR'
from enum import Enum
class RoleEnum(str, Enum):
    admin = "admin"
    parent = "parent"
PYR

cat > app/db/models/tipo_membresia.py << 'PYM'
from enum import Enum
class TipoMembresiaEnum(str, Enum):
    basico = "basico"
    estandar = "estandar"
    premium = "premium"
PYM

cat > app/db/models/usuario.py << 'PYU'
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from .tipo_membresia import TipoMembresiaEnum
from .role import RoleEnum

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    email: str
    hashed_password: str
    role: RoleEnum = RoleEnum.parent
    tipo_membresia: TipoMembresiaEnum = TipoMembresiaEnum.basico
    is_active: bool = True

    hijos: List["Hijo"] = Relationship(back_populates="padre")
    direcciones: List["Direccion"] = Relationship(back_populates="padre")
PYU

# ======================================================
# MODELOS BASE
# ======================================================
cat > app/db/models/role.py << 'PYR'
from enum import Enum
class RoleEnum(str, Enum):
    admin = "admin"
    parent = "parent"
PYR

cat > app/db/models/tipo_membresia.py << 'PYM'
from enum import Enum
class TipoMembresiaEnum(str, Enum):
    basico = "basico"
    estandar = "estandar"
    premium = "premium"
PYM

cat > app/db/models/usuario.py << 'PYU'
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from .tipo_membresia import TipoMembresiaEnum
from .role import RoleEnum

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    email: str
    hashed_password: str
    role: RoleEnum = RoleEnum.parent
    tipo_membresia: TipoMembresiaEnum = TipoMembresiaEnum.basico
    is_active: bool = True

    hijos: List["Hijo"] = Relationship(back_populates="padre")
    direcciones: List["Direccion"] = Relationship(back_populates="padre")
PYU

# ======================================================
# MODELOS RESTANTES
# ======================================================

# --- Hijo ---
cat > app/db/models/hijo.py << 'PYH'
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Hijo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    edad: int
    padre_id: int = Field(foreign_key="usuario.id")

    padre: "Usuario" = Relationship(back_populates="hijos")
    loncheras: List["Lonchera"] = Relationship(back_populates="hijo")
PYH

# --- Alimento ---
cat > app/db/models/alimento.py << 'PYA'
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Alimento(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    calorias: int
    tipo: str

    lonchera_alimentos: List["LoncheraAlimento"] = Relationship(back_populates="alimento")
PYA

# --- Lonchera ---
cat > app/db/models/lonchera.py << 'PYL'
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Lonchera(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    hijo_id: int = Field(foreign_key="hijo.id")

    hijo: "Hijo" = Relationship(back_populates="loncheras")
    lonchera_alimentos: List["LoncheraAlimento"] = Relationship(back_populates="lonchera")
PYL

# --- Lonchera_Alimento ---
cat > app/db/models/lonchera_alimento.py << 'PYLA'
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class LoncheraAlimento(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    lonchera_id: int = Field(foreign_key="lonchera.id")
    alimento_id: int = Field(foreign_key="alimento.id")
    cantidad: int

    lonchera: "Lonchera" = Relationship(back_populates="lonchera_alimentos")
    alimento: "Alimento" = Relationship(back_populates="lonchera_alimentos")
PYLA

# --- Dirección ---
cat > app/db/models/direccion.py << 'PYD'
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class Direccion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ciudad: str
    direccion: str
    padre_id: int = Field(foreign_key="usuario.id")

    padre: "Usuario" = Relationship(back_populates="direcciones")
PYD

# --- Restricción ---
cat > app/db/models/restriccion.py << 'PYR2'
from typing import Optional
from sqlmodel import SQLModel, Field

class Restriccion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    descripcion: str
PYR2

# --- Excepción ---
cat > app/db/models/excepcion.py << 'PYE'
from typing import Optional
from sqlmodel import SQLModel, Field

class Excepcion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    motivo: str
    detalle: str
PYE

# --- Inventario ---
cat > app/db/models/inventario.py << 'PYI'
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Inventario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    cantidad_total: int

    movimientos: List["InventarioMovimiento"] = Relationship(back_populates="inventario")
PYI

# --- InventarioMovimiento ---
cat > app/db/models/inventario_movimiento.py << 'PYIM'
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class InventarioMovimiento(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tipo: str  # entrada o salida
    cantidad: int
    inventario_id: int = Field(foreign_key="inventario.id")

    inventario: "Inventario" = Relationship(back_populates="movimientos")
PYIM

# --- HistorialAlimento ---
cat > app/db/models/historial_alimento.py << 'PYHA'
from typing import Optional
from sqlmodel import SQLModel, Field

class HistorialAlimento(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    alimento_id: int
    fecha_consumo: str
    observaciones: str
PYHA

# ======================================================
# SCHEMAS (Pydantic/SQLModel)
# ======================================================
cat > app/schemas/__init__.py << 'PYSC'
from sqlmodel import SQLModel

class ResponseMessage(SQLModel):
    message: str
PYSC


# ======================================================
# CRUD BÁSICO DE EJEMPLO (Usuario)
# ======================================================
cat > app/crud/usuario.py << 'PYCRUD'
from sqlmodel import Session, select
from app.db.models.usuario import Usuario

def get_usuarios(session: Session):
    return session.exec(select(Usuario)).all()

def get_usuario(session: Session, user_id: int):
    return session.get(Usuario, user_id)

def create_usuario(session: Session, usuario: Usuario):
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario

def delete_usuario(session: Session, user_id: int):
    usuario = session.get(Usuario, user_id)
    if usuario:
        session.delete(usuario)
        session.commit()
    return usuario
PYCRUD


# ======================================================
# ROUTER DE EJEMPLO (Usuario)
# ======================================================
cat > app/api/v1/routers/usuarios.py << 'PYROUT'
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.database import engine
from app.db.models.usuario import Usuario
from app.crud.usuario import get_usuarios, create_usuario, get_usuario, delete_usuario

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

def get_session():
    with Session(engine) as session:
        yield session

@router.get("/", response_model=list[Usuario])
def listar_usuarios(session: Session = Depends(get_session)):
    return get_usuarios(session)

@router.get("/{user_id}", response_model=Usuario)
def obtener_usuario(user_id: int, session: Session = Depends(get_session)):
    usuario = get_usuario(session, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.post("/", response_model=Usuario)
def crear_usuario(usuario: Usuario, session: Session = Depends(get_session)):
    return create_usuario(session, usuario)

@router.delete("/{user_id}", response_model=dict)
def eliminar_usuario(user_id: int, session: Session = Depends(get_session)):
    usuario = delete_usuario(session, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado correctamente"}
PYROUT


# ======================================================
# MAIN APP — Punto de entrada
# ======================================================
cat > app/main.py << 'PYMAIN'
from fastapi import FastAPI
from app.core.config import settings
from app.db.database import create_db_and_tables
from app.api.v1.routers import usuarios

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.include_router(usuarios.router, prefix="/api/v1")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "Bienvenido a NutriBox API v2"}
PYMAIN


# ======================================================
# CRUD Y ROUTERS AUTOMÁTICOS PARA TODOS LOS MODELOS
# ======================================================

# Crear CRUD genérico
cat > app/crud/base.py << 'PYBASE'
from typing import Type, TypeVar, List
from sqlmodel import Session, SQLModel, select

ModelType = TypeVar("ModelType", bound=SQLModel)

class CRUDBase:
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_all(self, session: Session) -> List[ModelType]:
        return session.exec(select(self.model)).all()

    def get(self, session: Session, id: int) -> ModelType | None:
        return session.get(self.model, id)

    def create(self, session: Session, obj: ModelType) -> ModelType:
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    def delete(self, session: Session, id: int) -> bool:
        db_obj = session.get(self.model, id)
        if db_obj:
            session.delete(db_obj)
            session.commit()
            return True
        return False
PYBASE

# Generar CRUD y router para cada modelo automáticamente
for model in hijo alimento lonchera alimento lonchera_alimento direccion restriccion excepcion inventario inventario_movimiento historial_alimento; do
cat > app/crud/${model}.py << PYCRUD
from sqlmodel import Session
from app.db.models.${model} import ${model^}
from app.crud.base import CRUDBase

crud_${model} = CRUDBase(${model^})
PYCRUD

cat > app/api/v1/routers/${model}s.py << PYROUT
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.database import engine
from app.db.models.${model} import ${model^}
from app.crud.${model} import crud_${model}

router = APIRouter(prefix="/${model}s", tags=["${model^}"])

def get_session():
    with Session(engine) as session:
        yield session

@router.get("/", response_model=list[${model^}])
def listar(session: Session = Depends(get_session)):
    return crud_${model}.get_all(session)

@router.get("/{id}", response_model=${model^})
def obtener(id: int, session: Session = Depends(get_session)):
    obj = crud_${model}.get(session, id)
    if not obj:
        raise HTTPException(status_code=404, detail="${model^} no encontrado")
    return obj

@router.post("/", response_model=${model^})
def crear(obj: ${model^}, session: Session = Depends(get_session)):
    return crud_${model}.create(session, obj)

@router.delete("/{id}")
def eliminar(id: int, session: Session = Depends(get_session)):
    eliminado = crud_${model}.delete(session, id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="${model^} no encontrado")
    return {"message": "${model^} eliminado correctamente"}
PYROUT
done

# ======================================================
# ACTUALIZAR MAIN PARA INCLUIR TODOS LOS ROUTERS
# ======================================================
cat > app/main.py << 'PYMAIN'
from fastapi import FastAPI
from app.core.config import settings
from app.db.database import create_db_and_tables
from app.api.v1.routers import usuarios
from importlib import import_module
import pkgutil

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# Cargar routers dinámicamente
for _, module_name, _ in pkgutil.iter_modules(['app/api/v1/routers']):
    if module_name != "__init__":
        module = import_module(f"app.api.v1.routers.{module_name}")
        app.include_router(module.router, prefix="/api/v1")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "NutriBox API v2 funcionando correctamente ���"}
PYMAIN
