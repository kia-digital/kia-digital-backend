from dotenv import load_dotenv
from fastapi import APIRouter, Depends,HTTPException,status
from service.ui_service import UIService
from sqlalchemy.orm import Session
from lib.db_init import get_db

import os

load_dotenv()

class DataUIController:
    def __init__(self):
        URL_PATH = os.getenv("URL_PATH")
        self.router = APIRouter(prefix=f"{URL_PATH}")
        self.router.add_api_route("/marital-status",self.marital_status,methods=["GET"])
        self.router.add_api_route("/roles",self.roles,methods=["GET"])
        self.router.add_api_route("/relationships",self.relationship,methods=["GET"])
        self.router.add_api_route("/status-inquiry",self.status_inquiry,methods=["GET"])
        self.router.add_api_route("/type-blood-pressure",self.get_type_blood_pressure,methods=["GET"])
        self.router.add_api_route("/type-inquiry",self.getTypeInquiry,methods=["GET"])
        self.router.add_api_route("/users",self.getAllUser,methods=["GET"])
        
    
    def getAllUser(self,db: Session= Depends(get_db)):
        response = UIService.getAllUser(db)
        if response:
            raise HTTPException( status_code= status.HTTP_200_OK, detail= response )
        else:
            raise HTTPException( 
                status_code= status.HTTP_404_NOT_FOUND, 
                detail= {
                        "status" : "failed",
                        "message": "user data not available",
                        "data": None
                }
            )
    
    def getTypeInquiry(self,db: Session = Depends(get_db)):
        response = UIService.getTypeInquiry(db)
        if response:
            raise HTTPException( status_code= status.HTTP_200_OK, detail= response )
        else:
            raise HTTPException( 
                status_code= status.HTTP_404_NOT_FOUND, 
                detail= {
                        "status" : "failed",
                        "message": "role data not available",
                        "data": None
                }
            )
    
    def get_type_blood_pressure(self,db: Session= Depends(get_db)):
        response = UIService.get_type_blood_pressure(db)
        if response:
            raise HTTPException( status_code= status.HTTP_200_OK, detail= response )
        else:
            raise HTTPException( 
                status_code= status.HTTP_404_NOT_FOUND, 
                detail= {
                        "status" : "failed",
                        "message": "role data not available",
                        "data": None
                }
            )
        
    def marital_status(self,db: Session = Depends(get_db)):
        response = UIService.get_roles(db)
        if response:
            raise HTTPException( status_code= status.HTTP_200_OK, detail= response )
        else:
            raise HTTPException( 
                status_code= status.HTTP_404_NOT_FOUND, 
                detail= {
                        "status" : "failed",
                        "message": "role data not available",
                        "data": None
                }
            )

        
    def roles(self, db:Session = Depends(get_db)):
        response = UIService.get_roles(db)
        
        if response:
            raise HTTPException( status_code= status.HTTP_200_OK, detail= response )
        else:
            raise HTTPException( 
                status_code= status.HTTP_404_NOT_FOUND, 
                detail= {
                        "status" : "failed",
                        "message": "role data not available",
                        "data": None
                }
            )
    
    def relationship( self, db: Session = Depends(get_db)):
        response = UIService.get_relationship(db)
        
        if response:
            raise HTTPException( status_code= status.HTTP_200_OK, detail= response )
        else:
            raise HTTPException( 
                status_code= status.HTTP_404_NOT_FOUND, 
                detail= {
                        "status" : "failed",
                        "message": "relationship data not available",
                        "data": None
                }
            )
            
    def status_inquiry( self, db: Session = Depends(get_db) ):
        response = UIService.get_status_inquiry(db)
        
        if response:
            raise HTTPException( status_code= status.HTTP_200_OK, detail= response )
        else:
            raise HTTPException( 
                status_code= status.HTTP_404_NOT_FOUND, 
                detail= {
                        "status" : "failed",
                        "message": "status inquiry data not available",
                        "data": None
                }
            )
        