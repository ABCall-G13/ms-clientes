from pydantic import BaseModel, EmailStr

class ClienteCreate(BaseModel):
    nombre: str
    email: EmailStr
    nit: str
    direccion: str
    telefono: str
    industria: str

    class Config:
        from_attributes = True  # Esto reemplaza orm_mode en Pydantic V2

class ClienteResponse(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    nit: str
    direccion: str
    telefono: str
    industria: str

    class Config:
        from_attributes = True