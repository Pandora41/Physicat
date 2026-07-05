# Application Configuration - Pydantic v2 settings management with environment variable support and type validation

from functools import lru_cache
from pathlib import Path
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

    mail_server: Optional[str] = Field(default=None, description="SMTP server hostname")
    mail_port: int = Field(default=587, description="SMTP server port")
    mail_username: Optional[str] = Field(default=None, description="SMTP username")
    mail_password: Optional[str] = Field(default=None, description="SMTP password")
    mail_use_tls: bool = Field(default=True, description="Use TLS for SMTP")
    mail_use_ssl: bool = Field(default=False, description="Use SSL for SMTP")
    mail_default_sender: str = Field(default="noreply@physicat.local", description="Default sender email")


    cors_origins: Optional[str] = Field(
        default=None, description="CORS allowed origins (comma-separated)"
    )

    # Resolve relative SQLite paths against the project root to avoid using the current working directory.
    def _resolve_database_url(self, database_url: str) -> str:
        if not database_url.startswith("sqlite:///"):
            return database_url

        sqlite_path = database_url[len("sqlite:///"):]
        if sqlite_path in {":memory:", ":memory"}:
            return database_url

        if Path(sqlite_path).is_absolute() or sqlite_path.startswith("/"):
            return database_url

        project_root = Path(__file__).resolve().parents[1]
        resolved_path = (project_root / sqlite_path).resolve()
        return f"sqlite:///{resolved_path.as_posix()}"

    # Get SQLAlchemy configuration dictionary
    def get_sqlalchemy_config(self) -> dict[str, Any]:
        return {
            "SQLALCHEMY_DATABASE_URI": self._resolve_database_url(self.database_url),
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "SQLALCHEMY_ECHO": self.database_echo,
        }


# Get cached settings instance (uses LRU cache to ensure settings are loaded only once per process)
@lru_cache()
def get_settings() -> Settings:
    return Settings()

