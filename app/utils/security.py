import base64
import json
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app import config
from app.db.session import get_db
from app.models.cliente import Cliente
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

SECRET_KEY = config.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login-client")

def get_current_user(request: Request, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Intenta obtener el token de Authorization o X-Forwarded-Authorization
    token =  request.headers.get("X-Forwarded-Authorization") or request.headers.get("Authorization")
    
    if not token or not token.startswith("Bearer "):
        raise credentials_exception
    
    # Elimina el prefijo 'Bearer ' del token
    token = token[7:]
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Busca al usuario en la base de datos
    user = db.query(Cliente).filter(Cliente.email == email).first()
    if user is None:
        raise credentials_exception
    return user