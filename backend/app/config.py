import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    DYNAMODB_TABLE: str = os.getenv("DYNAMODB_TABLE", "UrlShortener")
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8000")

    class Config:
        env_file = ".env"

settings = Settings()