import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
load_dotenv()

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: int
    database_password: str
    database_name: str
    database_username: str

    class Config:
        env_file = ".env" ## pydantic will look in .envfile 

settings = Settings()