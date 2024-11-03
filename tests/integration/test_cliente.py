import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.db.session import get_db
from app.utils.security import get_current_user
from main import app
from app.models.cliente import Cliente

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    # Eliminar todas las tablas antes de la prueba
    Base.metadata.drop_all(bind=engine)
    # Crear las tablas nuevamente
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    # Mockear get_current_user para evitar la autenticación real
    def mock_get_current_user():
        # Retorna un usuario simulado
        return Cliente(
            id=1,
            nombre="Usuario Simulado",
            email="simulado@xyz.com",
            nit="123456789",
            direccion="Calle Falsa 123",
            telefono="555-1234",
            industria="Tecnología",
            password="hashedpassword"
        )

    # Sobrescribir la dependencia get_current_user
    app.dependency_overrides[get_db] = lambda: session
    app.dependency_overrides[get_current_user] = mock_get_current_user

    yield TestClient(app)

    # Limpiar overrides después de las pruebas
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
    cliente_data_1 = {
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
    cliente_data_2 = {
        "nombre": "Empresa ABC",
        "email": "empresa@abc.com",
        "nit": "123456789",
        "direccion": "Avenida Siempre Viva 742",
        "telefono": "555-5678",
        "industria": "Tecnología",
        "password": "Secreto$2",
        "WelcomeMessage": "Bienvenido a la empresa ABC",
        "escalation_time": 24
    }
    client.post("/clientes/", json=cliente_data_1)
    client.post("/clientes/", json=cliente_data_2)
    response = client.get("/clientes/")
    assert response.status_code == 200
    clientes = response.json()
    assert len(clientes) == 2
    assert clientes[0]["email"] == cliente_data_1["email"]
    assert clientes[1]["email"] == cliente_data_2["email"]

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
