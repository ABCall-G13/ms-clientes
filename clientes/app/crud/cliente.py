from sqlalchemy.orm import Session
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate

def create_cliente(db: Session, cliente: ClienteCreate):
    db_cliente = Cliente(
        nombre=cliente.nombre,
        email=cliente.email,
        direccion=cliente.direccion,
        telefono=cliente.telefono
    )
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente
