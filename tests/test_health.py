# Tests for Health Check Endpoints - tests for health and readiness endpoints
import pytest
from flask import Flask


# Test health check endpoint returns healthy status
def test_health_check(client) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert data["service"] == "flask-api"


# Test readiness check when database is connected
def test_readiness_check_healthy(client, app: Flask, reset_db) -> None:
    with app.app_context():
        from app import db

        # Ensure database is accessible
        db.session.execute(db.text("SELECT 1"))

    response = client.get("/ready")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ready"
    assert data["database"] == "connected"


# Test root endpoint returns OK status
def test_root_endpoint(client) -> None:
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert "message" in data


# Test readiness check when database connection fails
def test_readiness_check_database_error(client, app: Flask, reset_db, monkeypatch) -> None:
    with app.app_context():
        from app import db
        
        # Mock db.session.execute to raise an exception
        def mock_execute(*args, **kwargs):
            raise Exception("Database connection failed")
        
        monkeypatch.setattr(db.session, "execute", mock_execute)
    
    response = client.get("/ready")
    assert response.status_code == 503
    data = response.get_json()
    assert data["status"] == "not_ready"
    assert data["database"] == "disconnected"

