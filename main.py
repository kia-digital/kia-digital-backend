from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import create_engine

from controller.auth_controller import AuthController
import os
from model.base import Base

load_dotenv()

app = FastAPI() 

# DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine("postgresql+psycopg2://postgres:anggara123@localhost/kia")
Base.metadata.create_all(engine)

auth_controller = AuthController()
app.include_router(auth_controller.router)