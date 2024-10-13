from pydantic import BaseModel, EmailStr

# Esquema para crear un nuevo cliente
class ClienteCreate(BaseModel):
    nombre: str
    email: EmailStr
    direccion: str
    telefono: str

    class Config:
        orm_mode = True
