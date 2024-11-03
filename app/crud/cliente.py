from sqlalchemy.orm import Session
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def create_cliente(db: Session, cliente: ClienteCreate):
    hashed_password = get_password_hash(cliente.password)
    db_cliente = Cliente(
        nombre=cliente.nombre,
        email=cliente.email,
        nit=cliente.nit,
        direccion=cliente.direccion,
        telefono=cliente.telefono,
        industria=cliente.industria,
        password=hashed_password,
        WelcomeMessage=cliente.WelcomeMessage,
        escalation_time=cliente.escalation_time,
        session=db
    )
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente


def get_all_clientes(db: Session):
    return db.query(Cliente).all()


def get_cliente_by_nit(db: Session, nit: str):
    return db.query(Cliente).filter(Cliente.nit == nit).first()
