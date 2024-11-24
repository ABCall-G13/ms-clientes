from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.cliente import Cliente
from app.schemas.auth import LoginRequest
from app.schemas.cliente import ClienteCreate
from passlib.context import CryptContext
from app.utils.security import create_access_token, verify_password

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

def get_cliente_by_email(db: Session, email: str):
    return db.query(Cliente).filter(Cliente.email == email).first()

def authenticate_cliente(db: Session, login_request: LoginRequest):
    cliente = db.query(Cliente).filter(Cliente.email == login_request.email).first()
    if not cliente or not verify_password(login_request.password, cliente.password):
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos")
    
    access_token = create_access_token(data={"sub": cliente.email})
    return {"access_token": access_token, "token_type": "bearer"}

 
 
def actualizar_plan(db: Session, cliente: Cliente, plan: str):
    cliente.plan = plan
    db.commit()
    db.refresh(cliente)
    return cliente

