import os
from pydantic_settings import BaseSettings
from pydantic import validator
from typing import List


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

def get_url():
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    server = os.getenv("POSTGRES_SERVER")
    port = os.getenv("POSTGRES_PORT")
    db = os.getenv("POSTGRES_DB")
    return f"postgresql+asyncpg://{user}:{password}@{server}:{port}/{db}"

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[str] = []
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    LOGGING_CONFIG_FILE: str = os.path.join(BASE_DIR, 'logging.ini')
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_db_connection(cls, v, values):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    POSTGRES_DATABASE_URI: str = get_url()

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra='ignore'

settings = Settings()
