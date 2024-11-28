from pydantic import BaseModel

class FacturaCreate(BaseModel):
    cliente_nit: str
    fecha_inicio: str
    fecha_fin: str
    monto_base: float
    monto_adicional: float
    monto_total: float
    estado: str = "pendiente"
    cliente_id: int