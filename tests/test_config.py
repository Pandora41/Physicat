# Tests for Configuration Module - tests for the Pydantic settings configuration
import pytest
from app.config import Settings, get_settings


# Test that settings have correct default values (verifies Settings class provides sensible defaults)
@pytest.mark.unit
def test_settings_defaults() -> None:
    settings = Settings()
    assert settings.flask_env == "development"
    assert settings.port == 5000
    assert settings.host == "0.0.0.0"
    assert settings.log_level == "INFO"


# Test that settings can be loaded from environment variables
@pytest.mark.unit
def test_settings_from_env(monkeypatch) -> None:
    monkeypatch.setenv("FLASK_ENV", "production")
    monkeypatch.setenv("PORT", "8080")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")

    settings = Settings()
    assert settings.flask_env == "production"
    assert settings.port == 8080
    assert settings.log_level == "DEBUG"


# Test that get_settings returns cached instance (verifies LRU cache is working correctly)
@pytest.mark.unit
def test_get_settings_cached() -> None:
    settings1 = get_settings()
    settings2 = get_settings()
    assert settings1 is settings2


# Test SQLAlchemy configuration method (verifies get_sqlalchemy_config returns correct dictionary structure)
@pytest.mark.unit
def test_sqlalchemy_config() -> None:
    settings = Settings()
    config = settings.get_sqlalchemy_config()
    assert "SQLALCHEMY_DATABASE_URI" in config
    assert "SQLALCHEMY_TRACK_MODIFICATIONS" in config
    assert "SQLALCHEMY_ECHO" in config
    assert config["SQLALCHEMY_TRACK_MODIFICATIONS"] is False

