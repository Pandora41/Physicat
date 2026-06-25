# Pages Routes - serves HTML pages
from typing import Dict, Any

import structlog
from flask import Blueprint, render_template

logger = structlog.get_logger(__name__)

bp = Blueprint("pages", __name__)


# Home page
@bp.route("/", methods=["GET"])
def index() -> str:
    logger.info("Home page requested")
    return render_template("index.html", message="Welcome!")


# About page
@bp.route("/about", methods=["GET"])
def about() -> str:
    logger.info("About page requested")
    return render_template("about.html")

# Toc page
@bp.route("/toc", methods=["GET"])
def toc() -> str:
    logger.info("Toc page requested")
    return render_template("toc.html")

# Wave pages
@bp.route("/wave/learn", methods=["GET"])
def wave_learn() -> str:
    logger.info("Wave learn page requested")
    return render_template("wave/learn.html")

@bp.route("/wave/quiz", methods=["GET"])
def quiz_wave() -> str:
    logger.info("Wave quiz page requested")
    return render_template("wave/quiz.html")