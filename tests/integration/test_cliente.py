import pytest
import os
from fastapi.testclient import TestClient

# Import the SQLAlchemy parts
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from main import app
from app.db.base import Base
from app.db.session import get_db

# Create the new database session

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    # Crea las tablas antes de cada prueba
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

        # Elimina el archivo de la base de datos después de que terminen las pruebas
        if os.path.exists("test.db"):
            os.remove("test.db")


@pytest.fixture()
def client(session):

    # Dependency override

    def override_get_db():
        try:

            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


def test_create_cliente(client):
    cliente_data = {
        "nombre": "Empresa XYZ",
        "email": "empresa@xyz.com",
        "nit": "987654321",
        "direccion": "Calle Falsa 123",
        "telefono": "555-1234",
        "industria": "Finanzas",
        "password": "Secreto$1",
        "WelcomeMessage": "Bienvenido a la empresa XYZ"
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
        "WelcomeMessage": "Bienvenido a la empresa XYZ"
    }
    cliente_data_2 = {
        "nombre": "Empresa ABC",
        "email": "empresa@abc.com",
        "nit": "123456789",
        "direccion": "Avenida Siempre Viva 742",
        "telefono": "555-5678",
        "industria": "Tecnología",
        "password": "Secreto$2",
        "WelcomeMessage": "Bienvenido a la empresa ABC"
    }
    client.post("/clientes/", json=cliente_data_1)
    client.post("/clientes/", json=cliente_data_2)
    response = client.get("/clientes/")
    assert response.status_code == 200
    clientes = response.json()
    assert len(clientes) == 2
    assert clientes[0]["email"] == cliente_data_1["email"]
    assert clientes[1]["email"] == cliente_data_2["email"]
