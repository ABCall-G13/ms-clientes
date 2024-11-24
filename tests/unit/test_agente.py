import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
from app.db.base import Base
from app.crud.agente import create_agente, authenticate_agente, get_agente_by_email
from app.schemas.agente import AgenteCreate, AgenteLogin
from app.models.agente import Agente

@pytest.fixture(scope='module')
def db_engine():
    engine = create_engine("sqlite:///:memory:", echo=True)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

@pytest.fixture(scope='function')
def db_session(db_engine):
    SessionLocal = sessionmaker(bind=db_engine)
    session = SessionLocal()
    yield session
    session.close()

def test_create_agente(db_session):
    agente_data = AgenteCreate(
        nombre="Agente Uno",
        correo="agente1@example.com",
        password="strongpassword"
    )
    agente = create_agente(db_session, agente_data)
    assert agente.id is not None
    assert agente.correo == agente_data.correo

def test_create_agente_duplicate_correo(db_session):
    agente_data = AgenteCreate(
        nombre="Agente Dos",
        correo="agente1@example.com",  # Duplicate correo
        password="anotherpassword"
    )
    with pytest.raises(ValueError):
        create_agente(db_session, agente_data)

def test_authenticate_agente_success(db_session):
    agente_data = AgenteCreate(
        nombre="Agente Tres",
        correo="agente3@example.com",
        password="securepassword"
    )
    create_agente(db_session, agente_data)
    login_data = AgenteLogin(
        correo="agente3@example.com",
        password="securepassword"
    )
    result = authenticate_agente(db_session, login_data.correo, login_data.password)
    assert "access_token" in result
    assert result["token_type"] == "bearer"

def test_authenticate_agente_failure(db_session):
    login_data = AgenteLogin(
        correo="nonexistent@example.com",
        password="wrongpassword"
    )
    with pytest.raises(HTTPException):
        authenticate_agente(db_session, login_data.correo, login_data.password)

def test_get_agente_by_email(db_session):
    agente_data = AgenteCreate(
        nombre="Agente Cuatro",
        correo="agente4@example.com",
        password="securepassword",
    )

    create_agente(db_session, agente_data)
    agente = get_agente_by_email(db_session, email=agente_data.correo)
    assert agente is not None
    assert agente.correo == agente_data.correo
    assert agente.nombre == agente_data.nombre


def test_get_agente_by_nonexistent_email(db_session):
    agente = get_agente_by_email(db_session, email="nonexistent@example.com")
    assert agente is None