from sqlalchemy.orm import Session
from app.models.agente import Agente
from app.schemas.agente import AgenteCreate
from passlib.context import CryptContext
from fastapi import HTTPException
from app.utils.security import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_agente(db: Session, agente: AgenteCreate) -> Agente:
    hashed_password = get_password_hash(agente.password)
    db_agente = Agente(
        nombre=agente.nombre,
        correo=agente.correo,
        password=hashed_password
    )
    db.add(db_agente)
    try:
        db.commit()
        db.refresh(db_agente)
    except Exception as e:
        db.rollback()
        raise ValueError(str(e))
    return db_agente

def authenticate_agente(db: Session, correo: str, password: str) -> dict:
    agente = db.query(Agente).filter(Agente.correo == correo).first()
    if not agente or not agente.verify_password(password):
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos")
    
    access_token = create_access_token(data={"sub": agente.correo})
    return {"access_token": access_token, "token_type": "bearer"}

def get_agente_by_email(db: Session, email: str) -> Agente:
    return db.query(Agente).filter(Agente.correo == email).first()