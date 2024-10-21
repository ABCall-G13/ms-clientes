from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from clientes.app.routers import cliente
from clientes.app.db.session import engine
from clientes.app.db.base import Base

origins = [
    "http://localhost:3000",
]


def recreate_database():
    print("Recreating the database...")
    Base.metadata.create_all(engine)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cliente.router)


if __name__ == "__main__":
    recreate_database()
