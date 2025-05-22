from fastapi import HTTPException,status
from model.model import User,engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from service.auth_service import AuthService
import bcrypt
import psycopg2

class UserService:
    
    @classmethod
    def registrasi_account(cls,data: dict,db: Session):
        if data:
            password = str(data["password"]).encode("utf-8")
            password_hash = bcrypt.hashpw(password,bcrypt.gensalt(14)).decode()
            try:
                
                new_account = User(
                        name=data["name"],
                        email=data["email"],
                        password = password_hash)
                db.add(new_account)
                db.commit()
                db.refresh(new_account)
                
                return {"status": "success","message":"success registered account"}
            
            except IntegrityError as e:
                db.rollback()
                if isinstance(e.orig, psycopg2.errors.UniqueViolation):
                    return {"status": "failed","message":"email already exist"}
                return {"status": "failed","message":"failed for registered account"}
                
        else:
            return {"status": "failed","message":"failed for registered account"}
    
    @classmethod
    def check_isAvalibale(cls,data: dict,db: Session):
        user = db.query(User).filter_by(email=data["email"]).first()
        stored_password = user.password.encode()
        input_password = data["password"].encode("utf-8")
        
        if user:
          if bcrypt.checkpw(input_password,stored_password):
            token = AuthService.create_token({"user_id":user.id})
            raise HTTPException(
                status_code=status.HTTP_202_ACCEPTED,
                detail={
                        "status": "success",
                        "message": "login success",
                        "token": token
            })
          else:
            raise HTTPException(
                status_code=status.HTTP_202_ACCEPTED,
                detail={
                        "status": "failed",
                        "message": "password wrong",
                        "token": None
            })  
            
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail={
                                    "status": "failed",
                                    "message": "account is not registered",
                                    "token": None
                                })