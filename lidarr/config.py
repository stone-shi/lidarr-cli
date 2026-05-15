import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    lidarr_url: str = Field(..., alias="LIDARR_URL")
    lidarr_api_key: str = Field(..., alias="LIDARR_API_KEY")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
