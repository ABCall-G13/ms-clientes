from sqlalchemy import Column, Integer, String, Enum
from app.db.base import Base
from sqlalchemy.orm import validates
import enum

class PlanEnum(enum.Enum):
    emprendedor = "Emprendedor"
    empresario = "Empresario"
    empresario_plus = "Empresario Plus"

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(60), index=True)
    email = Column(String(60), unique=True, index=True)
    nit = Column(String(60), unique=True, index=True)
    direccion = Column(String(60))
    telefono = Column(String(60))
    industria = Column(String(60))
    password = Column(String(128), nullable=False)
    WelcomeMessage = Column(String)
    escalation_time = Column(Integer)
    plan = Column(Enum(PlanEnum))

    def __init__(self, **kwargs):
        self.session = kwargs.pop('session', None)
        super().__init__(**kwargs)

    @validates('nit')
    def validate_nit(self, key, value):
        if not value.isdigit():
            raise ValueError("El NIT debe ser numérico.")

        if self.session:
            existing_nit = self.session.query(Cliente).filter(Cliente.nit == value).first()
            if existing_nit:
                raise ValueError("El cliente con ese NIT ya está registrado.")
        
        return value

    @validates('email')
    def validate_email(self, key, value):
        if "@" not in value or "." not in value:
            raise ValueError("El correo electrónico no es válido.")
        
        # Verificar si ya existe un cliente con el mismo correo
        if self.session:
            existing_email = self.session.query(Cliente).filter(Cliente.email == value).first()
            if existing_email:
                raise ValueError("El cliente con ese correo ya está registrado.")
        
        return value
