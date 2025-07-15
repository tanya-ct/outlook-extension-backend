from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings 
from urllib.parse import quote

encoded_password = quote(settings.database_password)

DATABASE_URL = (
    f"postgresql://{settings.database_username}:{encoded_password}"
    f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
)
print("DATABASE_URL:", DATABASE_URL)
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base() ## models 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
## Fastapi dependency injection  