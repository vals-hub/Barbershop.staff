"""Application configuration settings loaded from environment variables."""
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration.

    Values are read from environment variables or a local `.env` file when present.
    Sensible defaults are provided so the demo API can run without additional
    configuration, while still advertising the variables that should be supplied
    in production.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = Field("Barbershop Booking API", alias="APP_NAME")
    environment: str = Field("development", alias="ENVIRONMENT")
    secret_key: str = Field("change-me", alias="SECRET_KEY")
    database_url: str = Field("sqlite:///./demo.db", alias="DATABASE_URL")
    access_token_expire_minutes: int = Field(60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    jwt_algorithm: str = Field("HS256", alias="JWT_ALGORITHM")


@lru_cache()
def get_settings() -> Settings:
    """Return a cached instance of :class:`Settings`."""

    return Settings()


settings = get_settings()
