from fastapi import APIRouter, Depends, HTTPException
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.crud.cliente import authenticate_cliente, create_cliente, get_all_clientes, get_cliente_by_nit, get_password_hash, get_cliente_by_email
from app.models.cliente import Cliente
from app.routers.cliente import obtener_cliente_por_email
from app.schemas.auth import LoginRequest
from app.schemas.cliente import ClienteCreate, EmailRequest
from jose import jwt

from app.utils.security import create_access_token, get_current_user, verify_password


@pytest.fixture(scope='module')
def db_engine():
    engine = create_engine("sqlite:///:memory:", echo=True)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(scope='function')
def db_session(db_engine):
    SessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=db_engine)
    session = SessionLocal()

    Base.metadata.drop_all(bind=db_engine)
    Base.metadata.create_all(bind=db_engine)

    try:
        yield session
    finally:
        session.close()


def test_create_cliente(db_session):
    cliente_data = ClienteCreate(
        nombre="John Doe",
        email="john.doe@example.com",
        nit="123456789",
        direccion="123 Main St",
        telefono="555-1234",
        industria="Tech",
        password="mysecretpassword",
        WelcomeMessage="Welcome John!",
        escalation_time=24
    )

    cliente = create_cliente(db_session, cliente_data)

    assert cliente.email == cliente_data.email
    assert cliente.nombre == cliente_data.nombre


def test_get_all_clientes(db_session):
    cliente_data_1 = ClienteCreate(
        nombre="John Doe",
        email="john.doe@example.com",
        nit="123456789",
        direccion="123 Main St",
        telefono="555-1234",
        industria="Tech",
        password="mysecretpassword",
        WelcomeMessage="Welcome John!",
        escalation_time=24
    )
    cliente_data_2 = ClienteCreate(
        nombre="Jane Doe",
        email="jane.doe@example.com",
        nit="987654321",
        direccion="456 Elm St",
        telefono="555-5678",
        industria="Health",
        password="anothersecretpassword",
        WelcomeMessage="Welcome Jane!",
        escalation_time=24
    )
    create_cliente(db_session, cliente_data_1)
    create_cliente(db_session, cliente_data_2)
    clientes = get_all_clientes(db_session)
    assert len(clientes) == 2
    assert clientes[0].email == cliente_data_1.email
    assert clientes[1].email == cliente_data_2.email


def test_get_cliente_by_nit(db_session):
    # Crear un cliente en la base de datos
    cliente_data = ClienteCreate(
        nombre="Empresa XYZ",
        email="empresa@xyz.com",
        nit="987654321",
        direccion="Calle Falsa 123",
        telefono="555-1234",
        industria="Finanzas",
        password="Secreto$1",
        WelcomeMessage="Bienvenido a la empresa XYZ",
        escalation_time=24
    )
    cliente = create_cliente(db_session, cliente_data)

    # Verificar que el cliente existe consultando por el NIT
    cliente_obtenido = get_cliente_by_nit(db_session, nit="987654321")
    assert cliente_obtenido is not None
    assert cliente_obtenido.nombre == cliente_data.nombre

    # Verificar que un NIT inexistente retorna None
    cliente_inexistente = get_cliente_by_nit(db_session, nit="000000000")
    assert cliente_inexistente is None

def test_obtener_cliente_por_email(db_session):
    # Crear un cliente en la base de datos
    cliente_data = ClienteCreate(
        nombre="Empresa XYZ",
        email="empresa@xyz.com",
        nit="987654321",
        direccion="Calle Falsa 123",
        telefono="555-1234",
        industria="Finanzas",
        password="Secreto$1",
        WelcomeMessage="Bienvenido a la empresa XYZ",
        escalation_time=24
    )
    cliente = create_cliente(db_session, cliente_data)

    # Verificar que el cliente existe consultando por el email
    cliente_obtenido = get_cliente_by_email(db_session, email="empresa@xyz.com")
    assert cliente_obtenido is not None
    assert cliente_obtenido.nombre == cliente_data.nombre

    # Verificar que un email inexistente retorna None
    cliente_inexistente = get_cliente_by_email(db_session, email="noexiste@xyz.com")
    assert cliente_inexistente is None

def test_create_cliente_with_duplicate_email(db_session):
    cliente_data = ClienteCreate(
        nombre="John Doe",
        email="john.doe@example.com",
        nit="123456789",
        direccion="123 Main St",
        telefono="555-1234",
        industria="Tech",
        password="mysecretpassword",
        WelcomeMessage="Welcome John!",
        escalation_time=24
    )
    create_cliente(db_session, cliente_data)
    
    # Intentar crear un cliente con el mismo email debería fallar
    with pytest.raises(ValueError) as exc_info:
        create_cliente(db_session, cliente_data)
    assert "El cliente con ese correo ya está registrado" in str(exc_info.value)


def test_verify_password():
    password = "mysecretpassword"
    hashed_password = get_password_hash(password)

    # Verificar con la contraseña correcta
    assert verify_password("mysecretpassword", hashed_password)

    # Verificar con una contraseña incorrecta
    assert not verify_password("wrongpassword", hashed_password)


    
def test_authenticate_cliente(db_session):
    # Crear un cliente en la base de datos
    cliente_data = {
        "nombre": "John Doe",
        "email": "john.doe@example.com",
        "nit": "123456789",
        "direccion": "123 Main St",
        "telefono": "555-1234",
        "industria": "Tech",
        "password": get_password_hash("mysecretpassword"),
        "WelcomeMessage": "Welcome John!",
        "escalation_time": 24
    }
    cliente = Cliente(**cliente_data)
    db_session.add(cliente)
    db_session.commit()

    # Probar autenticación exitosa
    login_request = LoginRequest(email="john.doe@example.com", password="mysecretpassword")
    result = authenticate_cliente(db_session, login_request)
    assert "access_token" in result
    assert result["token_type"] == "bearer"

    # Probar autenticación fallida
    login_request = LoginRequest(email="john.doe@example.com", password="wrongpassword")
    with pytest.raises(HTTPException):
        authenticate_cliente(db_session, login_request)

def test_get_current_user(db_session):
    # Crear un cliente en la base de datos
    cliente_data = {
        "nombre": "John Doe",
        "email": "john.doe@example.com",
        "nit": "123456789",
        "direccion": "123 Main St",
        "telefono": "555-1234",
        "industria": "Tech",
        "password": get_password_hash("mysecretpassword"),
        "WelcomeMessage": "Welcome John!",
        "escalation_time": 24
    }
    cliente = Cliente(**cliente_data)
    db_session.add(cliente)
    db_session.commit()

    # Crear un token válido
    token_data = {"sub": "john.doe@example.com"}
    token = create_access_token(token_data)

    class MockRequest:
        headers = {
            "X-Forwarded-Authorization": f"Bearer {token}"
        }

    # Probar obtener usuario actual exitoso
    user = get_current_user(MockRequest(), db_session)
    assert user.email == "john.doe@example.com"

    # Probar obtener usuario actual fallido
    invalid_token = jwt.encode({"sub": "invalid@example.com"}, "your_secret_key", algorithm="HS256")
    class MockInvalidRequest:
        headers = {
            "X-Forwarded-Authorization": f"Bearer {invalid_token}"
        }
    with pytest.raises(HTTPException):
        get_current_user(MockInvalidRequest(), db_session)


def test_obtener_cliente_por_email_no_encontrado(db_session):
    # Crear un cliente en la base de datos
    cliente_data = ClienteCreate(
        nombre="John Doe",
        email="john.doe@example.com",
        nit="123456789",
        direccion="123 Main St",
        telefono="555-1234",
        industria="Tech",
        password="mysecretpassword",
        WelcomeMessage="Welcome John!",
        escalation_time=24
    )
    create_cliente(db_session, cliente_data)

    # Mockear una solicitud con un email inexistente
    class MockRequest:
        headers = {
            "X-Forwarded-Authorization": "Bearer invalid_token"
        }

    # Probar obtener cliente por email inexistente
    with pytest.raises(HTTPException):
        obtener_cliente_por_email(EmailRequest(email="sebas@gmail.com"), db_session, get_current_user(MockRequest(), db_session))
        


        