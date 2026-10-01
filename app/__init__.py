from __future__ import annotations

import os
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FastAPI Enterprise Customer API"
    app_version: str = "1.0.0"
    app_env: str = "development"
    debug: bool = True

    database_url: str = "sqlite:///./data/app.db"

    secret_key: str = Field(default="CHANGE_ME_IN_ENV")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    redis_url: str = "redis://localhost:6379/0"
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_topic: str = "customer-events"

    default_username: str = "admin"
    default_password: str = "admin123"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def is_prod(self) -> bool:
        return self.app_env.lower() == "production"


settings = Settings()
