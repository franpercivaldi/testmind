# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Jira configuration
    jira_api_base: str
    jira_email: str
    jira_token: str

    # PostgreSQL configuration
    postgres_host: str
    postgres_port: int
    postgres_name: str
    postgres_user: str
    postgres_password: str

    class Config:
        env_file = ".env"

settings = Settings()