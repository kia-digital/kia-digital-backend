from fastapi import APIRouter, Depends, HTTPException, Request,status,Header
import os
from sqlalchemy.orm import Session
from lib.db_init import get_db
from service.article_service import ArticleService
from service.auth_service import AuthService
from service.ml_service import MLService

class ArticleController:
    def __init__(self):
        URL_PATH = os.getenv("URL_PATH")
        self.router = APIRouter(prefix=f"{URL_PATH}/article")
        self.router.add_api_route("/",self.getAllArticle,methods=["GET"])
        self.router.add_api_route("/recom",self.getRecom,methods=["GET"])
        
    async def getRecom(self,trimester: int,authorization:str= Header(None),db: Session = Depends(get_db)): # type: ignore
        token = authorization.split(" ")[1]
        data_verify = AuthService.verify_token(token)
        
        if data_verify["status"] == 200:
            user_id = data_verify["payload"]["user_id"]    
            response = ArticleService.getRecommendation(user_id,trimester,db)  
            raise HTTPException(
                status_code= status.HTTP_200_OK,
                detail= response
            )
        
        else: 
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail= data_verify
            )        
        
    def getAllArticle(self):
        response = MLService.getAllArticles()

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