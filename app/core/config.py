# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    jira_api_base: str
    jira_email: str
    jira_token: str

    class Config:
        env_file = ".env"

settings = Settings()
