from fastapi import HTTPException,status
from model.model import User, Role,AccountVerification
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from service.auth_service import AuthService
from service.email_services import EmailService
import bcrypt
import psycopg2

class UserService:
    
    @classmethod
    async def registrasi_account(cls,data: dict,db: Session):
        if data:
            password = str(data["password"]).encode("utf-8")
            password_hash = bcrypt.hashpw(password,bcrypt.gensalt(14)).decode()
            
            try:
                new_account = User(
                        name=data["name"],
                        email=data["email"],
                        password = password_hash,
                        marital_status_id = data["marital_status"],
                        role_id = 1
                    )
                
                db.add(new_account)
                db.commit()
                db.refresh(new_account)
                
                user = db.query(User).filter(
                        User.email == data["email"],
                        User.password == password_hash
                    ).first()
                
                
                token_verification = AuthService.create_token({"user_id":user.id})
                
                account_verification = AccountVerification(
                    users_id = user.id,
                    token = token_verification,
                    verified = False
                )
                
                db.add(account_verification)
                db.commit()
                db.refresh(account_verification)
                
                await EmailService.send_email("Verifikasi Akun Kia Digital",user.email,token_verification,user.id)
                # close db
                db.close()
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
            account_isverified = (
                db.query(AccountVerification)
                .filter(AccountVerification.users_id == user.id)
                .first()    
            )
            
            if account_isverified.verified:
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
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                        "status": "failed",
                        "message": "account not verified",
                        "token": None
            })  
          else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
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
    
    @classmethod
    def verify_account_user(cls,db: Session,token: str,id: str):
        account_user_status = (
            db.query(AccountVerification)
            .filter(AccountVerification.users_id == id)
            .first()
        )
        
        db.close()
        
        if account_user_status.token == token and account_user_status:
            is_verified = AuthService.verify_token(token)
            response =  {
                    "status" : is_verified["status"],
                    "message" : is_verified["message"],
            }  
            
            if is_verified["status"] == 200:
                account_user_status.verified = True
                db.commit()
                return response
            else:
                return response   
                
        else:
            return response
        