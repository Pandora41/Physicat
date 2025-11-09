# API v1 Routes - main API endpoints for version 1 of the RESTful API
from typing import Dict, Any, List

import structlog
from flask import Blueprint, jsonify, request
from flasgger import swag_from

logger = structlog.get_logger(__name__)

bp = Blueprint("api_v1", __name__)


# API information endpoint - returns API version and available endpoints
@bp.route("/", methods=["GET"])
def api_info() -> Dict[str, Any]:
    logger.info("API info requested")
    return jsonify(
        {
            "version": "1.0.0",
            "endpoints": [
                "/api/v1/",
                "/api/v1/items",
                "/api/v1/items/<id>",
            ],
        }
    )


# Get all items - returns a list of all items in the system with pagination
@bp.route("/items", methods=["GET"])
def get_items() -> Dict[str, Any]:
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    logger.info("Items requested", page=page, per_page=per_page)

    # Placeholder response - replace with actual database query
    return jsonify(
        {
            "items": [],
            "total": 0,
            "page": page,
            "per_page": per_page,
        }
    )


# Get a specific item by ID
@bp.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id: int) -> Dict[str, Any]:
    logger.info("Item requested", item_id=item_id)

    # Placeholder response - replace with actual database query
    return jsonify({"id": item_id, "name": "Sample Item"}), 200


# Create a new item
@bp.route("/items", methods=["POST"])
def create_item() -> Dict[str, Any]:
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "Name is required"}), 400

    logger.info("Item creation requested", name=data.get("name"))

    # Placeholder response - replace with actual database insert
    return jsonify(
        {
            "id": 1,
            "name": data["name"],
            "message": "Item created successfully",
        }
    ), 201

