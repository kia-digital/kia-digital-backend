
import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Request, HTTPException, status
from lib.db_init import get_db
from service.user_service import UserService
from sqlalchemy.orm import Session

load_dotenv()

class AuthController:
    def __init__(self):
        URL_PATH = os.getenv("URL_PATH")
        self.router = APIRouter(prefix= f"{URL_PATH}/auth")
        self.router.add_api_route("/login",self.login,methods=["POST"])
        self.router.add_api_route("/register",self.register,methods=["POST"])
        self.router.add_api_route("/verify",self.verify,methods=["GET"])
    
    async def login(self,request: Request,db: Session = Depends(get_db)):
        body = await request.json()
        return UserService.check_isAvalibale(body,db)
    
    async def register(self,request: Request,db: Session = Depends(get_db)):
        body_request = await request.json()
        return await UserService.registrasi_account(body_request,db)
    
    async def verify(self,token: str, id: str,db: Session = Depends(get_db)):
        response = UserService.verify_account_user(db,token,id)
        if response["status"] == 200:
            raise HTTPException( status_code= status.HTTP_200_OK, detail= response)
        else:
            raise HTTPException( status_code= status.HTTP_401_UNAUTHORIZED, detail= response)
        