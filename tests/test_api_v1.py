# Tests for API v1 Endpoints - tests for the main API v1 endpoints
import pytest
from flask import Flask


# Test API info endpoint returns version and endpoints
def test_api_info(client) -> None:
    response = client.get("/api/v1/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["version"] == "1.0.0"
    assert "endpoints" in data
    assert isinstance(data["endpoints"], list)


# Test getting items when none exist
def test_get_items_empty(client) -> None:
    response = client.get("/api/v1/items")
    assert response.status_code == 200
    data = response.get_json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert data["items"] == []
    assert data["total"] == 0


# Test getting items with pagination parameters
def test_get_items_with_pagination(client) -> None:
    response = client.get("/api/v1/items?page=2&per_page=5")
    assert response.status_code == 200
    data = response.get_json()
    assert data["page"] == 2
    assert data["per_page"] == 5


# Test getting a specific item by ID
def test_get_item_by_id(client) -> None:
    response = client.get("/api/v1/items/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1
    assert "name" in data


# Test creating a new item successfully
def test_create_item_success(client) -> None:
    item_data = {"name": "Test Item", "description": "Test Description"}
    response = client.post(
        "/api/v1/items",
        json=item_data,
        content_type="application/json",
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Test Item"
    assert "id" in data
    assert "message" in data


# Test creating item without required name field
def test_create_item_missing_name(client) -> None:
    item_data = {"description": "Test Description"}
    response = client.post(
        "/api/v1/items",
        json=item_data,
        content_type="application/json",
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

