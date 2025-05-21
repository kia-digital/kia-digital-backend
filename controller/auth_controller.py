
import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Request
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
    
    async def login(self,request: Request,db: Session = Depends(get_db)):
        body = await request.json()
        return UserService.check_isAvalibale(body,db)
    
    async def register(self,request: Request,db: Session = Depends(get_db)):
        body_request = await request.json()
        
        print(body_request)
        
        return UserService.registrasi_account(body_request,db)
        
        