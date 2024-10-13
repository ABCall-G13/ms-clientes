
from fastapi import FastAPI
from clientes.app.routes import router as cliente_router

app = FastAPI()

app.include_router(cliente_router)