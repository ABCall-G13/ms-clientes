from fastapi import FastAPI
from app.routers import cliente
from app.db.session import engine
from app.db.base import Base

def recreate_database():
    print("Recreating the database...")
    Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(cliente.router)


if __name__ == "__main__":
    recreate_database()
