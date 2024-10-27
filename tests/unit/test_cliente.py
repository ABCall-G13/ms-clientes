import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.crud.cliente import create_cliente, get_all_clientes
from app.schemas.cliente import ClienteCreate


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