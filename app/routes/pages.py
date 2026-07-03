# Pages Routes - serves HTML pages
from typing import Dict, Any

import structlog
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from app.extensions import db
from app.models import User

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

# Projectile Motion Pages
@bp.route("/projectile_motion/learn", methods=["GET"])
def projectile_motion_learn() -> str:
    logger.info("projectile_motion learn page requested")
    return render_template("projectile_motion/learn.html")

@bp.route("/projectile_motion/quiz", methods=["GET"])
def quiz_projectile_motion() -> str:
    logger.info("projectile_motion quiz page requested")
    return render_template("projectile_motion/quiz.html")

@bp.route("/bb84", methods=["GET"])
def bb84() -> str:
    logger.info("BB84 dashboard requested")
    return render_template("bb84.html")


@bp.route("/register", methods=["GET", "POST"])
def register() -> str:
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not username or not email or not password or not confirm_password:
            flash("すべてのフィールドを入力してください。", "danger")
        elif password != confirm_password:
            flash("パスワードが一致しません。", "danger")
        elif User.query.filter_by(username=username).first():
            flash("このユーザー名は既に使われています。", "danger")
        elif User.query.filter_by(email=email).first():
            flash("このメールアドレスは既に使われています。", "danger")
        else:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("登録が完了しました。ログインしてください。", "success")
            return redirect(url_for("pages.login"))

    return render_template("register.html")


@bp.route("/login", methods=["GET", "POST"])
def login() -> str:
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session["user_id"] = user.id
            session["username"] = user.username
            session["is_admin"] = bool(user.is_admin)
            flash("ログインしました。", "success")
            return redirect(url_for("pages.toc"))

        flash("メールアドレスまたはパスワードが正しくありません。", "danger")

    return render_template("login.html")


@bp.route("/logout")
def logout() -> str:
    session.pop("user_id", None)
    session.pop("username", None)
    session.pop("is_admin", None)
    flash("ログアウトしました。", "success")
    return redirect(url_for("pages.index"))