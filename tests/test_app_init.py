# Tests for App Initialization - tests for Flask app factory and initialization
import builtins
import pytest

from app import create_app
from app.config import Settings


# Test create_app with default settings
@pytest.mark.unit
def test_create_app_default() -> None:
    app = create_app()
    assert app is not None
    assert app.config["TESTING"] is False


# Test create_app with custom settings
@pytest.mark.unit
def test_create_app_custom_settings() -> None:
    custom_settings = Settings(
        flask_env="testing",
        flask_debug=True,
        secret_key="custom-secret",
        database_url="sqlite:///:memory:",
    )
    
    app = create_app(custom_settings)
    assert app is not None
    assert app.config["SECRET_KEY"] == "custom-secret"
    assert app.config["DEBUG"] is True
    assert app.config["TESTING"] is True


# Test create_app handles ImportError when flasgger is not available
@pytest.mark.unit
def test_create_app_no_flasgger(monkeypatch) -> None:
    original_import = builtins.__import__

    def mock_import(name, *args, **kwargs):
        if name == "flasgger":
            raise ImportError("No module named 'flasgger'")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", mock_import)

    app_instance = create_app()
    assert app_instance is not None
    assert app_instance.config["SECRET_KEY"] is not None


# Test that app registers all blueprints
@pytest.mark.unit
def test_create_app_registers_blueprints() -> None:
    app = create_app()
    
    # Check that blueprints are registered
    blueprint_names = [bp.name for bp in app.blueprints.values()]
    assert "health" in blueprint_names
    assert "api_v1" in blueprint_names


# Test root route is registered
@pytest.mark.unit
def test_create_app_root_route() -> None:
    app = create_app()
    
    # Check root route exists
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "ok"

