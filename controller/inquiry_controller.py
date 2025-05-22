
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Header, Request,status
from sqlalchemy.orm import Session
from lib.db_init import get_db
from service.auth_service import AuthService
from service.inquiry_service import InquiryService
import os

load_dotenv()

class InquiryController:
    
    def __init__(self):
        URL_PATH = os.getenv("URL_PATH")
        self.router = APIRouter(prefix= f"{URL_PATH}/inquiry")
        self.router.add_api_route("/information",self.information_user,methods=["GET"])
    
    async def information_user(
        self,
        db:Session = Depends(get_db),
        authorization: str = Header(None)
    ):
        token = authorization.split(" ")[1]
        data_verify = AuthService.verify_token(token)
        if data_verify["status"] == 200:
            user_id = data_verify["payload"]["user_id"]
            response = InquiryService.get_information_mom(user_id,db)    
            
            raise HTTPException(
                status_code= status.HTTP_200_OK,
                detail= response
            )
        else: 
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail= data_verify
            )
        
        