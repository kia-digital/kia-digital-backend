
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Header, Request,status
from sqlalchemy.orm import Session
from lib.db_init import get_db
from service.anc_service import AncService
from service.auth_service import AuthService
from service.inquiry_information import InquiryService
from model.model import User
import os

from service.pemantauan_service import PemantauanService


load_dotenv()

class InquiryController:
    
    def __init__(self):
        URL_PATH = os.getenv("URL_PATH")
        self.router = APIRouter(prefix= f"{URL_PATH}/inquiry")
        self.router.add_api_route("/information",self.information_mom,methods=["GET"])
        self.router.add_api_route("/information/update-users",self.patch_information,methods=["PATCH"])
        self.router.add_api_route("/anc/add",self.addAnc,methods=["POST"])
        self.router.add_api_route("/anc/",self.getAllAnc,methods=["GET"])
        self.router.add_api_route("/pemantauan/add",self.addPemantauan,methods=["POST"])
        
    async def addPemantauan(self,req: Request,authorization: str = Header(None) ,db:Session = Depends(get_db)):
        token = authorization.split(" ")[1]
        body = await req.json()
        data_verify = AuthService.verify_token(token)
        if data_verify["status"] == 200:
            user_id = data_verify["payload"]["user_id"]    
            response = PemantauanService.addPemantauan(body,user_id,db)    
            raise HTTPException(
                status_code= status.HTTP_200_OK,
                detail= response
            )
        
        else: 
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail= data_verify
            )
        
    async def getAllAnc(self,authorization:str=Header(None),db:Session=Depends(get_db)):
        token = authorization.split(" ")[1]
        data_verify = AuthService.verify_token(token)
        if data_verify["status"] == 200:
            user_id = data_verify["payload"]["user_id"]    
            response = AncService.getAll(user_id,db)    
            raise HTTPException(
                status_code= status.HTTP_200_OK,
                detail= response
            )
        
        else: 
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail= data_verify
            )
    
    async def addAnc(self,req: Request,db: Session = Depends(get_db),authorization: str = Header(None)):
        token = authorization.split(" ")[1]
        body = await req.json()
        data_verify = AuthService.verify_token(token)
        if data_verify["status"] == 200:
            user_id = data_verify["payload"]["user_id"]    
            response = AncService.addAncReport(body,user_id,db)    
            raise HTTPException(
                status_code= status.HTTP_200_OK,
                detail= response
            )
        
        else: 
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail= data_verify
            )
    
    async def information_mom(
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
        
    async def patch_information(
        self,
        request: Request,
        db: Session = Depends(get_db),
        authorization : str = Header(None)
    ):
        token = authorization.split(" ")[1]
        data_verify = AuthService.verify_token(token)
        user_update = await request.json()
        
        if data_verify["status"] == 200:
            user_id = data_verify["payload"]["user_id"]    
            user = db.query(User).filter(User.id == user_id).first()
            
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
            
            for key,value in user_update.items():
                if hasattr(user,key):
                    setattr(user,key,value)
            
            db.add(user)
            db.commit()
            db.refresh(user)
            
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail={
                    "status":"success",
                    "message": "update information user success"
                }
            )
            
        else: 
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail= data_verify
            )