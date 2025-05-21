
import os
from dotenv import load_dotenv
from fastapi import APIRouter, Request

load_dotenv()

class AuthController:
    def __init__(self):
        URL_PATH = os.getenv("URL_PATH")
        self.router = APIRouter(prefix= f"{URL_PATH}/auth")
        self.router.add_api_route("/login",self.login,methods=["POST"])
        self.router.add_api_route("/register",self.register,methods=["POST"])
    
    async def login(self,request: Request):
        body = await request.json()
        
        return request
    
    async def register(self,request: Request):
        return request