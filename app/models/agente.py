from sqlalchemy import Column, Integer, String
from app.db.base import Base
from sqlalchemy.orm import validates
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Agente(Base):
    __tablename__ = "agentes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(60), index=True)
    correo = Column(String(60), unique=True, index=True)
    password = Column(String(128), nullable=False)

    def __init__(self, **kwargs):
        self.session = kwargs.pop('session', None)
        super().__init__(**kwargs)

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password)

    @validates('correo')
    def validate_correo(self, key, value):
        if "@" not in value or "." not in value:
            raise ValueError("El correo electrónico no es válido.")
        
        # Verificar si ya existe un agente con el mismo correo
        if self.session:
            existing_email = self.session.query(Agente).filter(Agente.correo == value).first()
            if existing_email:
                raise ValueError("El agente con ese correo ya está registrado.")
        
        return value