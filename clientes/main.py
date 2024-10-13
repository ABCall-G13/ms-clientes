# app/main.py
from fastapi import FastAPI
from app.routers import cliente

app = FastAPI()

app.include_router(cliente.router)