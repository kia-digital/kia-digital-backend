
from dotenv import load_dotenv
from fastapi_mail import FastMail,MessageSchema,ConnectionConfig, MessageType
import os

load_dotenv()

class EmailService:
    __MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    __MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    __MAIL_FROM = os.getenv("MAIL_FROM")
    __MAIL_PORT = int(os.getenv("MAIL_PORT"))
    __MAIL_SERVER = os.getenv("MAIL_SERVER")
    __MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME")
    
    @classmethod
    def __setupConfiguration(cls):
        conf = ConnectionConfig(
            MAIL_USERNAME = cls.__MAIL_USERNAME,
            MAIL_PASSWORD = cls.__MAIL_PASSWORD,
            MAIL_FROM = cls.__MAIL_FROM,
            MAIL_PORT = cls.__MAIL_PORT,
            MAIL_SERVER = cls.__MAIL_SERVER,
            MAIL_FROM_NAME = cls.__MAIL_FROM_NAME,
            MAIL_SSL_TLS = False,
            MAIL_STARTTLS = True,
            USE_CREDENTIALS = True,
        )
        
        return conf
    
    @classmethod
    async def send_email(cls, subject: str, email_to: str,token: str,id: str):
        verification_url = f"{os.getenv('HOST_SERVER')}{os.getenv('URL_PATH')}/auth/verify?token={token}&id={id}"
        
        message = MessageSchema(
            subject = subject,
            recipients = [email_to],
            body = f"Click link berikut untuk verifikasi email kamu: {verification_url}",
            subtype = MessageType.plain
        )
        
        fastmail = FastMail(cls.__setupConfiguration())
        
        await fastmail.send_message(message)
    
    