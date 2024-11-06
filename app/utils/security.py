import base64
import json
from fastapi import Depends, HTTPException, Request
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app import config
from app.db.session import get_db
from app.models.cliente import Cliente

SECRET_KEY = config.SECRET_KEY
ALGORITHM = "HS256"

def get_current_user(request: Request, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    print("Headers received:", request.headers)

    user_info_encoded = request.headers.get("X-Endpoint-API-UserInfo")
    if user_info_encoded:
        try:
            user_info_json = base64.urlsafe_b64decode(user_info_encoded).decode("utf-8")
            user_info = json.loads(user_info_json)
            email = user_info.get("email")
            print("Decoded user info:", user_info)
        except (ValueError, json.JSONDecodeError):
            raise credentials_exception
    else:
        # Fallback to Authorization header
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            raise credentials_exception
        token = token[7:]
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            print("JWT payload:", payload) 
        except JWTError:
            raise credentials_exception
    
    # Look up user in the database
    user = db.query(Cliente).filter(Cliente.email == email).first()
    if user is None:
        raise credentials_exception
    return user
