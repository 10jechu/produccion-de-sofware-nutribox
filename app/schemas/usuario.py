from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UsuarioCreate(BaseModel):
    # Acepta 'email' o 'correo' en input; internamente usa 'email'
    email: EmailStr = Field(alias='correo')
    password: str = Field(min_length=8, alias='contrasena')
    nombre: str = Field(min_length=2)

    # Permite poblar por alias o por nombre de campo
    model_config = ConfigDict(populate_by_name=True)

class UsuarioLogin(BaseModel):
    email: EmailStr = Field(alias='correo')
    password: str = Field(min_length=8, alias='contrasena')
    model_config = ConfigDict(populate_by_name=True)

class UsuarioRead(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)
