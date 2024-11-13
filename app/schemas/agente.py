from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class AgenteCreate(BaseModel):
    nombre: str
    correo: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)

class AgenteResponse(BaseModel):
    id: int
    nombre: str
    correo: EmailStr

    model_config = ConfigDict(from_attributes=True)

class AgenteLogin(BaseModel):
    correo: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)