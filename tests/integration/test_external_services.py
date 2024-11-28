import pytest
import responses
from unittest.mock import patch
from app.external_services.factura import crear_factura
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate


@pytest.fixture
def cliente_data():
    return ClienteCreate(
        nombre="Empresa XYZ",
        email="simulado@xyz.com",
        nit="123456789",
        direccion="Calle Falsa 123",
        telefono="555-1234",
        industria="Tecnología",
        password="Secreto$1",
        WelcomeMessage="Bienvenido a la empresa XYZ",
        escalation_time=24
    )

@responses.activate
@patch('app.crud.cliente.create_cliente')
def test_crear_factura(mock_create_cliente, cliente_data):
    # Crear un cliente de prueba
    cliente = Cliente(
        id=1,
        nombre=cliente_data.nombre,
        email=cliente_data.email,
        nit=cliente_data.nit,
        direccion=cliente_data.direccion,
        telefono=cliente_data.telefono,
        industria=cliente_data.industria,
        password=cliente_data.password,
        WelcomeMessage=cliente_data.WelcomeMessage,
        escalation_time=cliente_data.escalation_time
    )
    mock_create_cliente.return_value = cliente

    # Simular la respuesta del servicio externo
    responses.add(
        responses.POST,
        "https://ms-facturacion-345518488840.us-central1.run.app/facturas",
        json={"id": "factura123", "status": "created"},
        status=201
    )

    # Llamar a la función crear_factura
    plan = "empresario_plus"
    factura_response = crear_factura(cliente, plan)

    # Verificar que la factura se haya creado correctamente
    assert factura_response["cliente_nit"] == "123456789"