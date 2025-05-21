from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
import os
import jwt

load_dotenv()

secret_key= os.getenv("JWT")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_jwt_token(data: dict):
    to_encode = data.copy()
    expire = datetime.timetz() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt

def verify_jwt_token(token: str):
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        return decoded_token if decoded_token["exp"] >= datetime.utcnow() else None
    except jwt.PyJWTError:
        return None