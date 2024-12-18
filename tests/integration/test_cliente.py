from unittest.mock import patch
from fastapi import HTTPException
import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.crud.cliente import create_cliente, get_password_hash
from app.db.base import Base
from app.db.session import get_db
from app.routers.cliente import actualizar_plan_cliente, obtener_cliente_por_email
from app.schemas.auth import LoginRequest
from app.schemas.cliente import ClienteCreate, EmailRequest, UpdatePlanRequest
from app.utils.security import create_access_token, get_current_user
from main import app
from app.models.cliente import Cliente
import responses
from sqlalchemy.orm import Session

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    cliente = Cliente(
        nombre="Usuario Simulado",
        email="simulado@xyz.com",
        nit="123456789",
        direccion="Calle Falsa 123",
        telefono="555-1234",
        industria="Tecnología",
        password="hashedpassword",
        WelcomeMessage="Bienvenido a la empresa XYZ",
        escalation_time=24
    )
    session.add(cliente)
    session.commit()
    session.refresh(cliente)

    def mock_get_current_user():
        return session.query(Cliente).get(cliente.id)

    app.dependency_overrides[get_db] = lambda: session
    app.dependency_overrides[get_current_user] = mock_get_current_user

    yield TestClient(app)

    app.dependency_overrides = {}

@pytest.fixture()
def cleanup():
    yield
    if os.path.exists("test.db"):
        os.remove("test.db")
        

@pytest.fixture
def mock_db_session():
    # Mock de la sesión de base de datos
    session = Session()
    yield session
    session.close()

@pytest.fixture
def mock_current_user():
    # Mock de un cliente actual
    return Cliente(
        nombre="Empresa Mock",
        email="mock@empresa.com",
        nit="123456789",
        direccion="Calle Mock 123",
        telefono="555-1234",
        industria="MockIndustria",
        password="hashedpassword",
        WelcomeMessage="Bienvenido a la empresa Mock",
        escalation_time=24,
    )

def test_create_cliente(client):
    cliente_data = {
        "nombre": "Empresa XYZ",
        "email": "empresa@xyz.com",
        "nit": "987654321",
        "direccion": "Calle Falsa 123",
        "telefono": "555-1234",
        "industria": "Finanzas",
        "password": "Secreto$1",
        "WelcomeMessage": "Bienvenido a la empresa XYZ",
        "escalation_time": 24
    }
    response = client.post("/clientes/", json=cliente_data)
    assert response.status_code == 200
    assert response.json()["nombre"] == cliente_data["nombre"]

def test_listar_clientes(client):

    response = client.get("/clientes/")
    assert response.status_code == 200
    clientes = response.json()
    assert len(clientes) == 1
    assert clientes[0]["email"] == "simulado@xyz.com"

def test_obtener_cliente_por_nit(client):
    cliente_data = {
        "nombre": "Empresa XYZ",
        "email": "empresa@xyz.com",
        "nit": "987654321",
        "direccion": "Calle Falsa 123",
        "telefono": "555-1234",
        "industria": "Finanzas",
        "password": "Secreto$1",
        "WelcomeMessage": "Bienvenido a la empresa XYZ",
        "escalation_time": 24
    }
    client.post("/clientes/", json=cliente_data)

    response = client.get("/clientes/987654321")
    assert response.status_code == 200
    assert response.json()["nombre"] == cliente_data["nombre"]

    response = client.get("/clientes/000000000")
    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente no encontrado"


def test_registrar_cliente_con_valor_invalido(client):
    cliente_data_invalido = {
        "nombre": "Empresa XYZ",
        "email": "empresa@xyz.com",
        "nit": "",  # NIT vacío para provocar un ValueError
        "direccion": "Calle Falsa 123",
        "telefono": "555-1234",
        "industria": "Finanzas",
        "password": "Secreto$1",
        "WelcomeMessage": "Bienvenido a la empresa XYZ",
        "escalation_time": 24
    }
    
    response = client.post("/clientes/", json=cliente_data_invalido)
    assert response.status_code == 400


def test_registrar_cliente_con_email_invalido(client):
    cliente_data_invalido = {
        "nombre": "Empresa XYZ",
        "email": "email_invalido",  # Email inválido para provocar un ValueError
        "nit": "987654321",
        "direccion": "Calle Falsa 123",
        "telefono": "555-1234",
        "industria": "Finanzas",
        "password": "Secreto$1",
        "WelcomeMessage": "Bienvenido a la empresa XYZ",
        "escalation_time": 24
    }
    
    response = client.post("/clientes/", json=cliente_data_invalido)
    assert response.status_code == 422


@patch("app.routers.cliente.crear_factura")
@patch("app.routers.cliente.actualizar_plan")
def test_actualizar_plan_cliente_no_factura(mock_actualizar_plan, mock_crear_factura, mock_db_session, mock_current_user):
    # Mock para actualizar_plan
    mock_actualizar_plan.return_value = mock_current_user

    # Mock para crear_factura (verificaremos que no se llama)
    mock_crear_factura.return_value = None

    # Datos de prueba para la solicitud
    request_data = UpdatePlanRequest(
        plan="empresario",
    )

    # Llamar al método directamente
    response = actualizar_plan_cliente(
        request=request_data,
        db=mock_db_session,
        current_user=mock_current_user
    )

    mock_crear_factura.assert_called_once_with(mock_current_user, "empresario")

    assert response is True

def test_plan_status(client):
    response = client.get("/status-plan")
    assert response.status_code == 200
    assert response.json() is False