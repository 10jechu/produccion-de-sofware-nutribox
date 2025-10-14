from pydantic import BaseModel, EmailStr
from app.db.schemas.common import ORMModel

class UserRegister(BaseModel):
    nombre: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRead(ORMModel):
    id: int
    nombre: str
    email: EmailStr
    rol_id: int | None = None
    membresia_id: int | None = None

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
