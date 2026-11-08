"""All configuration from environment variables (Module 22, 27)."""
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TASKBOARD_", env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./taskboard.db"
    jwt_secret: SecretStr = SecretStr("dev-only-change-me-to-a-long-random-value!!")
    token_minutes: int = 30
    cors_origins: list[str] = ["http://localhost:3000"]


settings = Settings()
