from fastapi import HTTPException
import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.crud.cliente import create_cliente, get_password_hash
from app.db.base import Base
from app.db.session import get_db
from app.routers.cliente import obtener_cliente_por_email
from app.schemas.auth import LoginRequest
from app.schemas.cliente import ClienteCreate, EmailRequest
from app.utils.security import create_access_token, get_current_user
from main import app
from app.models.cliente import Cliente

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


def test_actualizar_plan_cliente(client):
    update_plan_data = {
        "plan": "Empresario Plus"
    }

    response = client.post("/clientes/update-plan", json=update_plan_data)
    assert response.status_code == 200

    cliente_actualizado = response.json()
    assert cliente_actualizado["plan"] == "Empresario Plus"
    

def test_plan_status(client):
    response = client.get("/status-plan")
    assert response.status_code == 200
    assert response.json() is False