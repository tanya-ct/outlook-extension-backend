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
    azure_client_id: str
    azure_client_secret: str
    azure_tenant_id: str
    azure_redirect_uri: str

    class Config:
        env_file = ".env" ## pydantic will look in .envfile 

settings = Settings()