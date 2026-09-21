from __future__ import annotations

import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "inventory"
    app_env: str = "local"
    database_url: str = "postgresql+psycopg://diwyanshuprasad@127.0.0.1:5432/inventory_db"
    otel_service_name: str = "inventory"
    otel_exporter_otlp_endpoint: str = "http://localhost:4318"
    port: int = 8091
    seed_on_startup: bool = False


@lru_cache
def get_settings() -> Settings:
    s = Settings()
    # Allow classic env names
    if url := os.getenv("DATABASE_URL"):
        object.__setattr__(s, "database_url", url)
    return s
