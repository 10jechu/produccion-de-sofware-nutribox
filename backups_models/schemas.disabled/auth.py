from typing import Annotated, Optional
from pydantic import BaseModel, Field, AliasChoices, EmailStr, ConfigDict, model_validator

class _CIBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    @model_validator(mode="before")
    @classmethod
    def _lower_keys(cls, v):
        if isinstance(v, dict):
            m = {(k.lower() if isinstance(k, str) else k): v for k, v in v.items()}
            if "nombre" in m and "full_name" not in m:
                m["full_name"] = m.pop("nombre")
            return m
        return v

class UserRegister(_CIBase):
    full_name: Annotated[str, Field(validation_alias=AliasChoices("full_name","nombre"), serialization_alias="full_name")]
    email: EmailStr
    password: str
    rol: str = "user"
    membresia: str = "free"

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
