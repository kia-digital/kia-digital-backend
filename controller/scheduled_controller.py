
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import os

from fastapi import APIRouter, Depends, HTTPException, Header, Request, status

from lib.db_init import get_db
from service.auth_service import AuthService
from service.scheduled_service import ScheduledService

load_dotenv()

class ScheduledController:
    def __init__(self):
        URL_PATH = os.getenv("URL_PATH")
        self.router = APIRouter(prefix= f"{URL_PATH}/scheduled")
        self.router.add_api_route("/add",self.addScheduled,methods=["POST"])
        self.router.add_api_route("/",self.getAllById,methods=["GET"])
        self.router.add_api_route("/{id}",self.getById,methods=["GET"])
        self.router.add_api_route("/",self.updateScheduled,methods=["PATCH"])

    async def addScheduled(
        self,
        request: Request,
        db: Session = Depends(get_db),
        authorization: str = Header(None)
    ):
        token = authorization.split(" ")[1]
        data_verify = AuthService.verify_token(token)
        request_body = await request.json()
        if data_verify["status"] == 200:
            response = ScheduledService.add_scheduled(request_body,db)
            raise HTTPException(
                status_code= status.HTTP_200_OK,
                detail= response
            )
        
        else: 
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail= data_verify
            )

    async def getAllById(
        self,
        db: Session = Depends(get_db),
        authorization: str = Header(None)
    ):
        token = authorization.split(" ")[1]
        data_verify = AuthService.verify_token(token)
        payload = data_verify["payload"]
        user_id = payload["user_id"]
        response = ScheduledService.getAllScheduledById(user_id,db)
        
        if data_verify["status"] == 200:
            raise HTTPException(
                status_code= status.HTTP_200_OK,
                detail= response
            )
        
        else: 
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail= data_verify
            )
            
    async def updateScheduled(
        self,
        id: str,
        requestBody: Request,
        db: Session = Depends(get_db),
        authorization: str = Header(None)
    ):
        token = authorization.split(" ")[1]
        data_verify = AuthService.verify_token(token)
        
        if data_verify["status"] != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=data_verify
            )

        body = await requestBody.json()

        response = ScheduledService.update_scheduled(id, body, db)

        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=response
        )
        
    async def getById(
        self,
        id: str,
        db: Session = Depends(get_db),
        authorization: str = Header(None)
    ):
        token = authorization.split(" ")[1]
        data_verify = AuthService.verify_token(token)
        
        if data_verify["status"] != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=data_verify
            )
        
        print(id)
        payload = data_verify["payload"]
        user_id = payload["user_id"]
        response = ScheduledService.getById(id,user_id,db)

        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=response
        )