from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "To-do List API"
    sqlalchemy_database_url: str
    jwt_key: str

    class Config:
        env_file = ".env"
        secrets_dir = '/var/run'


@lru_cache
def get_settings() -> Settings:
    return Settings()
