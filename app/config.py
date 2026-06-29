# Application Configuration - Pydantic v2 settings management with environment variable support and type validation

from functools import lru_cache
from typing import Any, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# Application settings with Pydantic v2 validation - all settings can be overridden via environment variables
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Flask Configuration
    flask_env: str = Field(default="development", description="Flask environment")
    flask_debug: bool = Field(default=False, description="Enable Flask debug mode")
    secret_key: str = Field(
        default="dev-secret-key-change-in-production",
        description="Flask secret key for sessions",
    )

    # Database Configuration
    database_url: str = Field(
        default="sqlite:///app.db",
        description="Database connection URL",
    )
    database_echo: bool = Field(
        default=False, description="Echo SQL queries to console"
    )

    # Server Configuration
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=5000, description="Server port")

    # Logging Configuration
    log_level: str = Field(default="INFO", description="Logging level")

    # API Configuration
    api_title: str = Field(
        default="Flask RESTful API", description="API title for documentation"
    )
    api_version: str = Field(default="1.0.0", description="API version")

    # CORS Configuration (if needed)
    cors_origins: Optional[str] = Field(
        default=None, description="CORS allowed origins (comma-separated)"
    )

    # Get SQLAlchemy configuration dictionary
    def get_sqlalchemy_config(self) -> dict[str, Any]:
        return {
            "SQLALCHEMY_DATABASE_URI": self.database_url,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "SQLALCHEMY_ECHO": self.database_echo,
        }


# Get cached settings instance (uses LRU cache to ensure settings are loaded only once per process)
@lru_cache()
def get_settings() -> Settings:
    return Settings()

