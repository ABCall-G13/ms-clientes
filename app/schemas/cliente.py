from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class ClienteCreate(BaseModel):
    nombre: str
    email: EmailStr
    nit: str
    direccion: str
    telefono: str
    industria: str
    password: str
    WelcomeMessage: str
    escalation_time: Optional[int] = 7

    model_config = ConfigDict(from_attributes=True)


class ClienteResponse(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    nit: str
    direccion: str
    telefono: str
    industria: str
    WelcomeMessage: str
    escalation_time: int

    model_config = ConfigDict(from_attributes=True)

class EmailRequest(BaseModel):
    email: str

    model_config = ConfigDict(from_attributes=True)
