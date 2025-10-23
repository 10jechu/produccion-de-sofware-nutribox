from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioUpdate(BaseModel):
    nombre: str | None = None
    email: EmailStr | None = None
    password: str | None = None

class UsuarioRead(UsuarioBase):
    id: int
    activo: bool
    rol_id: int
    membresia_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
