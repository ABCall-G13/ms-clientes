import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.crud.cliente import create_cliente
from app.schemas.cliente import ClienteCreate
from app.models.cliente import Cliente

# Crear un motor de base de datos en memoria para las pruebas


@pytest.fixture(scope='module')
def db_engine():
    engine = create_engine("sqlite:///:memory:", echo=True)
    # Crear las tablas necesarias en la base de datos en memoria
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

# Crear una sesión de base de datos que use la base de datos en memoria


@pytest.fixture(scope='function')
def db_session(db_engine):
    SessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=db_engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# Prueba para la creación de un cliente


def test_create_cliente(db_session):
    cliente_data = ClienteCreate(
        nombre="John Doe",
        email="john.doe@example.com",
        nit="123456789",
        direccion="123 Main St",
        telefono="555-1234",
        industria="Tech",
        password="mysecretpassword",
        WelcomeMessage="Welcome John!"
    )

    # Crear cliente usando la función que se está probando
    cliente = create_cliente(db_session, cliente_data)

    # Validar que el cliente se ha creado correctamente
    assert cliente.email == cliente_data.email
    assert cliente.nombre == cliente_data.nombre
