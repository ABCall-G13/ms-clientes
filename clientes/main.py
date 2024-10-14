# app/main.py
from fastapi import FastAPI
from app.routers import cliente
from app.db.session import engine
from app.db.base import Base

def recreate_database():
    Base.metadata.create_all(engine)

recreate_database()

app = FastAPI()

app.include_router(cliente.router)
print("main.py")