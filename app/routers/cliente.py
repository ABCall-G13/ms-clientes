# app/routers/clientes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.cliente import ClienteCreate, ClienteResponse
from app.crud.cliente import create_cliente
from app.db.session import get_db
from app.models.cliente import Cliente

router = APIRouter()


@router.post("/clientes/", response_model=ClienteResponse)
def registrar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    try:
        return create_cliente(db=db, cliente=cliente)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
