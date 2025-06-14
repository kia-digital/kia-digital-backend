import os

from fastapi import APIRouter, Depends, HTTPException, Header, Request,status

from lib.db_init import get_db
from service.auth_service import AuthService
from sqlalchemy.orm import Session

from service.emergency_contact_service import EmergencyContactService

class EmergencyContactController:
    
    def __init__(self):
        URL_PATH = os.getenv("URL_PATH")
        self.router = APIRouter(prefix= f"{URL_PATH}/emergency-contact")
        self.router.add_api_route("/update",self.updateEmergencyContact,methods=["PATCH"])
        
    async def updateEmergencyContact(
        self,
        req: Request,
        db: Session = Depends(get_db),
        authorization: str = Header(None)
    ):
        token = authorization.split(" ")[1]
        data_verify = AuthService.verify_token(token)
        body = await req.json()
        
        if data_verify["status"] == 200:
            user_id = data_verify["payload"]["user_id"]    
            response = EmergencyContactService.updateData(user_id,body,db)  
            raise HTTPException(
                status_code= status.HTTP_200_OK,
                detail= response
            )
        
        else: 
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail= data_verify
            )