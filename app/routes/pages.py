# Pages Routes - serves HTML pages
from typing import Dict, Any

import structlog
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from app.extensions import db
from app.models import User
from app.utils.email import generate_verification_token, send_verification_email, confirm_verification_token

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
        elif len(password) < 8:
            flash("パスワードは8文字以上である必要があります。", "danger")
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

            token = generate_verification_token(user.email)
            send_verification_email(user.email, token)

            flash("登録が完了しました。確認メールを送信しました。メールを確認してアカウントを有効化してください。", "success")
            return redirect(url_for("pages.login"))

    return render_template("register.html")


@bp.route("/verify/<token>", methods=["GET"])
def verify_email(token: str) -> str:
    try:
        email = confirm_verification_token(token)
    except Exception:
        flash("確認リンクが無効か期限切れです。", "danger")
        return render_template("verify.html", verified=False)

    user = User.query.filter_by(email=email).first()
    if not user:
        flash("確認対象のユーザーが見つかりません。", "danger")
        return render_template("verify.html", verified=False)

    if user.is_verified:
        flash("既にメールアドレスは確認済みです。", "info")
        return render_template("verify.html", verified=True)

    user.is_verified = True
    db.session.commit()
    flash("メールアドレスが確認されました。ログインできます。", "success")
    return render_template("verify.html", verified=True)


@bp.route("/login", methods=["GET", "POST"])
def login() -> str:
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()

        if user is None or not user.check_password(password):
            flash("メールアドレスまたはパスワードが正しくありません。", "danger")
        elif not user.is_verified:
            # ✅ GANTI INI: Redirect ke halaman khusus buat user yang belum verified
            flash("メールアドレスが確認されていません。", "warning")
            return render_template("login_unverified.html", email=email)
        else:
            session["user_id"] = user.id
            session["username"] = user.username
            session["is_admin"] = bool(user.is_admin)
            session["is_verified"] = bool(user.is_verified)
            flash("ログインしました。", "success")
            return redirect(url_for("pages.toc"))

    return render_template("login.html")

@bp.route("/resend-verification", methods=["GET", "POST"])
def resend_verification() -> str:
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        
        if not email:
            flash("メールアドレスを入力してください。", "danger")
            return render_template("resend_verification.html")
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash("メールアドレスが見つかりません。", "danger")
            return render_template("resend_verification.html")
        
        if user.is_verified:
            flash("このメールアドレスは既に確認済みです。ログインしてください。", "info")
            return redirect(url_for("pages.login"))
        
        # Generate token baru dan kirim email
        try:
            token = generate_verification_token(user.email)
            send_verification_email(user.email, token)
            flash("確認メールを再送信しました。メールを確認してください。", "success")
            return redirect(url_for("pages.login"))
        except Exception as e:
            print(f"❌ Gagal kirim email verifikasi: {str(e)}")
            flash("メールの送信に失敗しました。後でもう一度お試しください。", "danger")
            return render_template("resend_verification.html")
    
    return render_template("resend_verification.html")


@bp.route("/logout")
def logout() -> str:
    session.pop("user_id", None)
    session.pop("username", None)
    session.pop("is_admin", None)
    session.pop("is_verified", None)
    flash("ログアウトしました。", "success")
    return redirect(url_for("pages.index"))