from pydantic import BaseModel, EmailStr
from app.db.schemas.common import ORMModel

class UserRegister(BaseModel):
    nombre: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    nombre: str | None = None
    email: EmailStr | None = None
    activo: bool | None = None
    membresia_id: int | None = None

class UserRead(ORMModel):
    id: int
    nombre: str
    email: EmailStr
    activo: bool
    rol_id: int | None = None
    membresia_id: int | None = None

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
