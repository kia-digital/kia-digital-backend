from dotenv import load_dotenv
from fastapi import FastAPI
from controller.inquiry_controller import InquiryController
from controller.auth_controller import AuthController
from controller.data_ui_controller import DataUIController
from fastapi.middleware.cors import CORSMiddleware
import os

load_dotenv()

app = FastAPI() 

auth_controller = AuthController()
inquiry_controller = InquiryController()
data_ui_controller = DataUIController()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_controller.router)
app.include_router(inquiry_controller.router)
app.include_router(data_ui_controller.router)