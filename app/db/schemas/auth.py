
from pydantic import BaseModel, EmailStr, field_validator
from typing import Literal

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserRegister(BaseModel):
    nombre: str
    email: EmailStr
    password: str
    membresia: Literal["Free", "Premium"] = "Free"
    rol: Literal["Usuario", "Admin"] = "Usuario"

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        return v
