from pydantic import BaseModel, EmailStr


class ClienteCreate(BaseModel):
    nombre: str
    email: EmailStr
    nit: str
    direccion: str
    telefono: str
    industria: str
    password: str
    WelcomeMessage: str
    escalation_time: int

    class Config:
        from_attributes = True


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

    class Config:
        from_attributes = True
