from pydantic import BaseModel, EmailStr, Field

class Token(BaseModel):
    access_token: str
    token_type: str

class UserRegister(BaseModel):
    full_name: str = Field(min_length=2, alias="nombre")
    email: EmailStr
    password: str = Field(min_length=8, alias="contrasena")
    rol: str = Field(default="Usuario")
    membresia: str = Field(default="Free")
    
    class Config:
        populate_by_name = True
