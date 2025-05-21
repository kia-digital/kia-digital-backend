from dotenv import load_dotenv
from fastapi import Depends,HTTPException,status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime,timedelta
import os
import jwt

load_dotenv()

class AuthService:
    security = HTTPBearer()
    SECRET_KEY  = os.getenv("JWT")
    ALGORITHM  = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES  = 30
    
    
    @classmethod
    def create_token(cls,data: dict):
        to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp":expire})
        token = jwt.encode(to_encode,cls.SECRET_KEY,algorithm=cls.ALGORITHM)
        return token
    
    @classmethod
    def verify_token(cls,credentials: HTTPAuthorizationCredentials = Depends(security)):
        token = credentials.credentials
        try:
            payload = jwt.decode(token,cls.SECRET_KEY,algorithms=[cls.ALGORITHM])
            return { "status" : "success", "message": "login success", "token": payload }
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail= {
                    "status": "failed",
                    "message": "token expired",
                    "token" : None
                })
        
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail= {
                    "status": "failed",
                    "message": "token invalid",
                    "token" : None
                })