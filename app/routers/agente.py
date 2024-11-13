from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.agente import AgenteCreate, AgenteResponse, AgenteLogin
from app.crud.agente import create_agente, authenticate_agente
from app.db.session import get_db

router = APIRouter()

@router.post("/agentes/register", response_model=AgenteResponse)
def registrar_agente(agente: AgenteCreate, db: Session = Depends(get_db)):
    try:
        return create_agente(db=db, agente=agente)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/agentes/login")
def login_agente(login_data: AgenteLogin, db: Session = Depends(get_db)):
    return authenticate_agente(db, correo=login_data.correo, password=login_data.password)