from fastapi import requests
import httpx
from app.models.cliente import Cliente
from app.schemas.factura import FacturaCreate
from app.utils.fechas import calcular_fechas


def crear_factura(cliente: Cliente, plan: str):

    fecha_inicial, fecha_fin = calcular_fechas()
    
    factura_data = FacturaCreate(
        cliente_nit=cliente.nit,
        fecha_inicio=fecha_inicial,
        fecha_fin=fecha_fin,
        monto_base=calcular_monto_total(plan),
        monto_adicional=0.0,
        monto_total=0.0,
        cliente_id=cliente.id
    )
    
    try:
        response = httpx.post("https://ms-facturacion-345518488840.us-central1.run.app/facturas",
                                json=factura_data.model_dump(),
                                timeout=10.0)
        response.raise_for_status()  # Lanza una excepción si la respuesta no tiene un código 2xx
        return response.json()  # Retorna la respuesta en formato JSON
    except httpx.RequestError as e:
        raise ValueError(f"Error al conectar con el microservicio: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Error HTTP en la creación de factura: {e.response.status_code} - {e.response.text}")


def calcular_monto_total(plan: str) -> float:
    # 1 dólar = 4000 pesos
    montos = {
        "emprendedor": 40000,
        "empresario": 80000,
        "empresario_plus": 200000,
    }
    return montos[plan]