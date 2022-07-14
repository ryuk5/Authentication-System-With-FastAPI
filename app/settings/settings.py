from pydantic import BaseSettings
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()


TEMPLATES_PATH = './templates/email'

class Settings(BaseSettings):
    secret_key: str 
    algorithm: str
    access_token_expire_minutes: int

    email_reset_token_expire_minutes: int

    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    mail_from_name: str


settings = Settings()