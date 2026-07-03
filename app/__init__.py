# Flask Application Factory - creates Flask instances with proper configuration, blueprints, and extensions

from typing import Optional

import structlog
from flask import Flask
from app.extensions import db

from app.config import Settings, get_settings
from app.utils.logging import configure_logging


logger = structlog.get_logger(__name__)


def create_app(config: Optional[Settings] = None) -> Flask:
    settings = config or get_settings()

    # Configure structured logging
    configure_logging(settings.log_level)

    app = Flask(__name__)
    
    # Configure Flask from settings
    app.config.update(settings.get_sqlalchemy_config())
    app.config["SECRET_KEY"] = settings.secret_key
    app.config["DEBUG"] = settings.flask_debug
    app.config["TESTING"] = settings.flask_env == "testing"

    # Initialize extensions
    db.init_app(app)

    # ✅ Import models (biar SQLAlchemy tau)
    from app import models

    # ✅ Setup Admin Panel (Flask-Admin)
    from app.admin import setup_admin
    if setup_admin(app) is None:
        logger.warning("Admin panel disabled: Flask-Admin is not installed.")

    # Register blueprints
    from app.routes import health, api_v1, pages, lessons

    app.register_blueprint(health.bp)
    app.register_blueprint(api_v1.bp, url_prefix="/api/v1")
    app.register_blueprint(pages.bp, url_prefix="/")
    app.register_blueprint(lessons.bp, url_prefix="/")
    
    # Setup OpenAPI documentation
    try:
        from flasgger import Swagger

        swagger_config = {
            "headers": [],
            "specs": [
                {
                    "endpoint": "apispec",
                    "route": "/apispec.json",
                    "rule_filter": lambda rule: True,
                    "model_filter": lambda tag: True,
                }
            ],
            "static_url_path": "/flasgger_static",
            "swagger_ui": True,
            "specs_route": "/apidocs",
        }

        swagger_template = {
            "swagger": "2.0",
            "info": {
                "title": "Flask RESTful API",
                "description": "Production-ready RESTful API with Flask 3.x",
                "version": "1.0.0",
            },
            "basePath": "/api/v1",
            "schemes": ["http", "https"],
        }

        Swagger(app, config=swagger_config, template=swagger_template)
        logger.info("OpenAPI documentation initialized")
    except ImportError:
        logger.warning("Flasgger not available, skipping OpenAPI setup")

    # Health check endpoint
    @app.route("/")
    def root() -> dict[str, str]:
        return {"status": "ok", "message": "Flask API is running"}

    logger.info("Flask application created", env=settings.flask_env)

    return app