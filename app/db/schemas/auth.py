from pydantic import BaseModel, EmailStr, Field

class UserRegister(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(..., min_length=8)
    rol: str = "Usuario"
    membresia: str = "Free"

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: str | None = None
