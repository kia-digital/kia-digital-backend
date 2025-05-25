from dotenv import load_dotenv
from fastapi import FastAPI
from controller.inquiry_controller import InquiryController
from controller.auth_controller import AuthController
from controller.data_ui_controller import DataUIController
import os

load_dotenv()

app = FastAPI() 

auth_controller = AuthController()
inquiry_controller = InquiryController()
data_ui_controller = DataUIController()

app.include_router(auth_controller.router)
app.include_router(inquiry_controller.router)
app.include_router(data_ui_controller.router)