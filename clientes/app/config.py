import os
from dotenv import load_dotenv

load_dotenv()
DB_USER = os.getenv("DB_USER_PRIMARY","prueba")
DB_PASSWORD = os.getenv("DB_PASSWORD_PRIMARY","prueba")
DB_HOST = os.getenv("DB_HOST_PRIMARY","localhost")
DB_NAME = os.getenv("DB_NAME_PRIMARY","prueba")
DB_PORT = os.getenv("DB_PORT_PRIMARY","5432")
DB_SOCKET_PATH_PRIMARY = os.getenv("DB_SOCKET_PATH_PRIMARY", "")
