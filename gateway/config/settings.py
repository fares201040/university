import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from .env file."""

    KEYCLOAK_BASE_URL: str
    REALM_NAME: str
    CLIENT_ID: str
    CLIENT_SECRET: str
    ALGORITHMS: list[str]
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    DEBUG: bool

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


try:
    settings = Settings()
except Exception as e:
    raise RuntimeError(
        "Failed to load settings from .env file. Please ensure all required variables are set."
    ) from e
