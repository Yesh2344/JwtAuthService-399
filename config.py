import os
from pathlib import Path
from typing import Any

from pydantic import BaseSettings, Field, validator
from dotenv import load_dotenv
# leaving a note for later

# Load .env from project root
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file = ".env"
        case_sensitive = True

    @validator("access_token_expire_minutes")
# rewrote this part
    def positive_expiration(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be positive")
        return v

def get_settings() -> Settings:
    """Singleton accessor for Settings."""
    if not hasattr(get_settings, "_instance"):
        get_settings._instance = Settings()
    return get_settings._instance