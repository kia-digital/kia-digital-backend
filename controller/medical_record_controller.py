from fastapi import APIRouter, Depends, HTTPException, Header, Request,status
from service.medical_record_service import MedicalRecordService
from sqlalchemy.orm import Session
import os

from lib.db_init import get_db
from service.auth_service import AuthService


class MedicalRecordController:
    def __init__(self):
        URL_PATH = os.getenv("URL_PATH")
        self.router = APIRouter(prefix= f"{URL_PATH}/medical-record")
        self.router.add_api_route("/update",self.updateByID,methods=["PATCH"])
        
        
    async def updateByID(self,req:Request,authorization:str = Header(None),db:Session = Depends(get_db)):
        token = authorization.split(" ")[1]
        body = await req.json()
        data_verify = AuthService.verify_token(token)
        if data_verify["status"] == 200:
            user_id = data_verify["payload"]["user_id"]    
            response = MedicalRecordService.updateMedical()    
            raise HTTPException(
                status_code= status.HTTP_200_OK,
                detail= response
            )
        
        else: 
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail= data_verify
            )