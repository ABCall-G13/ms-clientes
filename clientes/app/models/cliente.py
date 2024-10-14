from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(60), index=True)
    email = Column(String(60), unique=True, index=True)
    nit = Column(String(60), unique=True, index=True)
    direccion = Column(String(60))
    telefono = Column(String(60))
    industria = Column(String(60))