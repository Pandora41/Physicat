# Tests for Dependency Injection Utilities - tests for dependency injection patterns
import pytest
from typing import Any

from app.utils.dependencies import get_db, get_settings, inject_dependencies


# Test get_db returns database instance
@pytest.mark.unit
def test_get_db(app) -> None:
    with app.app_context():
        db_instance = get_db()
        assert db_instance is not None
        # Verify it's the SQLAlchemy instance
        assert hasattr(db_instance, "session")


# Test get_settings returns settings instance
@pytest.mark.unit
def test_get_settings_dependency() -> None:
    settings = get_settings()
    assert settings is not None
    assert hasattr(settings, "flask_env")
    assert hasattr(settings, "port")


# Test inject_dependencies decorator injects dependencies
@pytest.mark.unit
def test_inject_dependencies_decorator() -> None:
    # Create a mock dependency factory
    call_count = {"count": 0}
    
    def mock_db_factory() -> str:
        call_count["count"] += 1
        return "mock_db"
    
    def mock_settings_factory() -> str:
        call_count["count"] += 1
        return "mock_settings"
    
    # Create a function that uses dependencies
    @inject_dependencies(db=mock_db_factory, settings=mock_settings_factory)
    def test_function(arg1: str, db: Any = None, settings: Any = None) -> dict[str, Any]:
        return {"arg1": arg1, "db": db, "settings": settings}
    
    # Call function without providing dependencies
    result = test_function("test_arg")
    
    assert result["arg1"] == "test_arg"
    assert result["db"] == "mock_db"
    assert result["settings"] == "mock_settings"
    assert call_count["count"] == 2


# Test inject_dependencies doesn't override provided dependencies
@pytest.mark.unit
def test_inject_dependencies_no_override() -> None:
    def mock_db_factory() -> str:
        return "factory_db"
    
    @inject_dependencies(db=mock_db_factory)
    def test_function(db: Any = None) -> Any:
        return db
    
    # Provide db explicitly
    result = test_function(db="provided_db")
    
    # Should use provided value, not factory
    assert result == "provided_db"


# Test inject_dependencies preserves function metadata
@pytest.mark.unit
def test_inject_dependencies_metadata() -> None:
    def mock_factory() -> str:
        return "mock"
    
    @inject_dependencies(dep=mock_factory)
    def documented_function() -> str:
        """This is a documented function."""
        return "test"
    
    assert documented_function.__name__ == "documented_function"
    assert documented_function.__doc__ == "This is a documented function."

