from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import create_engine
from controller.inquiry_controller import InquiryController
from controller.auth_controller import AuthController
import os

load_dotenv()

app = FastAPI() 

auth_controller = AuthController()
inquiry_controller = InquiryController()
app.include_router(auth_controller.router)
app.include_router(inquiry_controller.router)