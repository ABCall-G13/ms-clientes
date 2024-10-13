from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    nit = Column(String, unique=True, index=True)
    direccion = Column(String)
    telefono = Column(String)
    industria = Column(String)