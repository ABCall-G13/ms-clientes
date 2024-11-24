import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.db.session import get_db
from app.models.agente import Agente
from main import app

# Configuración de la base de datos de prueba
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
    agente = Agente(
        nombre="Agente Simulado",
        correo="agente@xyz.com",
        password="$2b$12$12345678hashedpassword",  # Contraseña simulada encriptada con bcrypt
        session=session
    )
    session.add(agente)
    session.commit()
    session.refresh(agente)

    app.dependency_overrides[get_db] = lambda: session

    yield TestClient(app)

    app.dependency_overrides = {}

@pytest.fixture()
def cleanup():
    yield
    if os.path.exists("test.db"):
        os.remove("test.db")

### TESTS ###

def test_registrar_agente(client):
    agente_data = {
        "nombre": "Agente XYZ",
        "correo": "nuevo@xyz.com",
        "password": "Secreto$1"
    }
    response = client.post("/agentes/register", json=agente_data)
    assert response.status_code == 200
    assert response.json()["nombre"] == agente_data["nombre"]

def test_registrar_agente_email_duplicado(client):
    agente_data = {
        "nombre": "Agente Duplicado",
        "correo": "agente@xyz.com",
        "password": "Secreto$1"
    }
    response = client.post("/agentes/register", json=agente_data)
    # coger el error de la respuesta
    assert response.status_code == 400

def test_obtener_agente_por_email(client):
    email_request = {
        "email": "agente@xyz.com"
    }
    response = client.post("/agentes/email", json=email_request)
    assert response.status_code == 200
    assert response.json()["correo"] == email_request["email"]

    email_request_invalido = {
        "email": "noexistente@xyz.com"
    }
    response = client.post("/agentes/email", json=email_request_invalido)
    assert response.status_code == 404
    assert response.json()["detail"] == "Agente no encontrado"

