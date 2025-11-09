# Pytest Configuration and Fixtures - provides shared fixtures and configuration for all tests
import pytest
from typing import Generator

from app import create_app, db
from app.config import Settings


# Create application instance for testing
@pytest.fixture
def app() -> Generator:
    # Use test configuration
    test_settings = Settings(
        flask_env="testing",
        flask_debug=True,
        database_url="sqlite:///:memory:",
        secret_key="test-secret-key",
    )

    app_instance = create_app(test_settings)
    
    # Ensure db is bound to this app instance
    with app_instance.app_context():
        # Create all tables
        db.create_all()
        yield app_instance
        # Clean up
        db.drop_all()
        db.session.remove()


# Create test client for making requests
@pytest.fixture
def client(app) -> Generator:
    with app.test_client() as client:
        yield client


# Create CLI test runner
@pytest.fixture
def runner(app) -> Generator:
    return app.test_cli_runner()


# Reset database before each test (only for tests that use the app fixture)
@pytest.fixture
def reset_db(app) -> Generator:
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield
        db.session.remove()

