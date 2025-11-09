# Health Check Routes - provides health check and readiness endpoints for monitoring
from typing import Dict, Any

import structlog
from flask import Blueprint, jsonify

from app import db

logger = structlog.get_logger(__name__)

bp = Blueprint("health", __name__)


# Health check endpoint - returns basic application health status
@bp.route("/health", methods=["GET"])
def health_check() -> Dict[str, Any]:
    logger.debug("Health check requested")
    return jsonify({"status": "healthy", "service": "flask-api"})


# Readiness check endpoint - checks if application is ready to serve traffic, including database connectivity
@bp.route("/ready", methods=["GET"])
def readiness_check() -> Dict[str, Any]:
    try:
        # Simple database connectivity check
        db.session.execute(db.text("SELECT 1"))
        db_status = "connected"
        status_code = 200
    except Exception as e:
        logger.error("Database connection failed", error=str(e))
        db_status = "disconnected"
        status_code = 503

    response_data = {
        "status": "ready" if status_code == 200 else "not_ready",
        "database": db_status,
    }

    return jsonify(response_data), status_code

