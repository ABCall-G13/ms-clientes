# app/routers/clientes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.cliente import ClienteCreate, ClienteResponse
from app.crud.cliente import create_cliente
from app.db.session import get_db

router = APIRouter()

@router.post("/clientes/", response_model=ClienteResponse)
def registrar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    # Verificar si ya existe un cliente con el mismo NIT o correo
    db_cliente = db.query(Cliente).filter(Cliente.nit == cliente.nit).first()
    if db_cliente:
        raise HTTPException(status_code=400, detail="El cliente con ese NIT ya está registrado.")
    
    return create_cliente(db=db, cliente=cliente)
