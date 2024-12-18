# app/routers/clientes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.external_services.factura import crear_factura
from app.models.cliente import Cliente
from app.schemas.auth import LoginRequest
from app.schemas.cliente import ClienteCreate, ClienteResponse, EmailRequest, UpdatePlanRequest
from app.crud.cliente import authenticate_cliente, create_cliente, get_all_clientes, get_cliente_by_nit, get_cliente_by_email, actualizar_plan
from app.db.session import get_db
from typing import List
from app.utils.security import get_current_user

router = APIRouter()

@router.post("/clientes", response_model=ClienteResponse)
def registrar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    try:
        return create_cliente(db=db, cliente=cliente)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/clientes", response_model=List[ClienteResponse])
def listar_clientes(db: Session = Depends(get_db)):
    return get_all_clientes(db)

@router.get("/clientes/{nit}", response_model=ClienteResponse)
def obtener_cliente_por_nit(nit: str, db: Session = Depends(get_db)):
    cliente = get_cliente_by_nit(db, nit=nit)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.post("/clientes/email", response_model=ClienteResponse)
def obtener_cliente_por_email(request: EmailRequest, db: Session = Depends(get_db)):
    cliente = get_cliente_by_email(db, email=request.email)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.post("/login-client")
def login_client(login_request: LoginRequest, db: Session = Depends(get_db)):
    return authenticate_cliente(db, login_request)

@router.post("/clientes/update-plan", response_model=bool)
def actualizar_plan_cliente(
    request: UpdatePlanRequest,
    db: Session = Depends(get_db),
    current_user: Cliente = Depends(get_current_user)
):

    try:
        cliente_actualizado = actualizar_plan(db, current_user, request.plan.value)
        crear_factura(cliente_actualizado, request.plan.value)
        return True
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/status-plan", response_model=bool)
def obtener_estado_plan_cliente(current_user: Cliente = Depends(get_current_user)):
    return current_user.plan is not None


@router.get("/current-client", response_model=int)
def obtener_id_cliente(current_user: Cliente = Depends(get_current_user)):
    return current_user.id
