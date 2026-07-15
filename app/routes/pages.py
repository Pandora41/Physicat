# Pages Routes - serves HTML pages
from typing import Dict, Any
import requests 
import os
import structlog
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from app.extensions import db
from app.models import User
from app.utils.email import (
    generate_verification_token,
    send_verification_email,
    confirm_verification_token,
    generate_password_reset_token,
    confirm_password_reset_token,
    send_password_reset_email,
)

logger = structlog.get_logger(__name__)

bp = Blueprint("pages", __name__)

site_key = os.environ.get('TURNSTILE_SITE_KEY', '')


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
    # 1. AMBIL KEY LANGSUNG DARI OS.ENVIRON (BIAR GAK NONE LAGI)
    site_key = os.environ.get('TURNSTILE_SITE_KEY', '')
    secret_key = os.environ.get('TURNSTILE_SECRET_KEY', '')

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        turnstile_token = request.form.get('cf-turnstile-response')

        if not turnstile_token:
            flash('Cloudflareの確認に失敗しました (Token kosong).', 'error')
            return redirect(url_for('pages.register'))
        
        verify_url = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'
        payload = {
            'secret': secret_key, # Pake variabel secret_key di atas
            'response': turnstile_token,
            'remoteip': request.remote_addr
        }
        
        try:
            response = requests.post(verify_url, data=payload, timeout=5)
            result = response.json()
            
            if not result.get('success'):
                print("❌ CLOUDFLARE API RESPONSE:", result) # DEBUG
                error_codes = result.get("error-codes", ["Unknown error"])
                flash(f'Cloudflareの確認に失敗しました: {error_codes}', 'error')
                return redirect(url_for('pages.register'))
                
        except Exception as e:
            # 2. INI BAKAL BILANG KENAPA ERROR "b" MUNCUL!
            print(f"❌ EXCEPTION SAAT REQUEST: {str(e)}") 
            flash(f'Cloudflareの確認に失敗しました (System Error): {str(e)}', 'error')
            return redirect(url_for('pages.register'))

        spam_domains = ['immenseignite.info', 'tempmail.com', 'guerrillamail.com']
        if any(email.endswith(f'@{domain}') for domain in spam_domains):
            flash("無効なメールアドレスです。", "error")
            return redirect(url_for('pages.register'))

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

    # 3. KIRIM site_key KE TEMPLATE (BIAR GAK ERROR "site_key not defined")
    return render_template("register.html", turnstile_site_key=site_key)


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


@bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password() -> str:
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()

        if not email:
            flash("メールアドレスを入力してください。", "danger")
            return render_template("forgot_password.html")

        user = User.query.filter_by(email=email).first()
        if user:
            try:
                token = generate_password_reset_token(user.email)
                send_password_reset_email(user.email, token)
            except Exception as exc:
                logger.exception("Password reset email failed", error=str(exc), email=email)

        flash("パスワード再設定用のメールを送信しました。メールボックスを確認してください。", "info")
        return redirect(url_for("pages.login"))

    return render_template("forgot_password.html")


@bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token: str) -> str:
    try:
        email = confirm_password_reset_token(token)
    except Exception:
        flash("このリンクは無効か期限切れです。", "danger")
        return redirect(url_for("pages.forgot_password"))

    user = User.query.filter_by(email=email).first()
    if not user:
        flash("ユーザーが見つかりませんでした。", "danger")
        return redirect(url_for("pages.forgot_password"))

    if request.method == "POST":
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not password or not confirm_password:
            flash("新しいパスワードを入力してください。", "danger")
        elif len(password) < 8:
            flash("パスワードは8文字以上である必要があります。", "danger")
        elif password != confirm_password:
            flash("パスワードが一致しません。", "danger")
        else:
            user.set_password(password)
            db.session.commit()
            flash("パスワードを変更しました。ログインしてください。", "success")
            return redirect(url_for("pages.login"))

    return render_template("reset_password.html", token=token)


@bp.route("/profile/edit", methods=["GET", "POST"])
def edit_profile() -> str:
    user_id = session.get("user_id")
    if not user_id:
        flash("ログインしてください。", "warning")
        return redirect(url_for("pages.login"))

    user = User.query.get(user_id)
    if not user:
        flash("ユーザー情報が見つかりません。", "danger")
        return redirect(url_for("pages.login"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        current_password = request.form.get("current_password", "")
        new_password = request.form.get("new_password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not username or not email:
            flash("ユーザー名とメールアドレスを入力してください。", "danger")
        else:
            existing_username = User.query.filter(User.id != user.id, User.username == username).first()
            existing_email = User.query.filter(User.id != user.id, User.email == email).first()

            if existing_username:
                flash("このユーザー名は既に使われています。", "danger")
            elif existing_email:
                flash("このメールアドレスは既に使われています。", "danger")
            else:
                changed_email = user.email != email
                user.username = username

                if changed_email:
                    user.email = email
                    user.is_verified = False
                    try:
                        token = generate_verification_token(user.email)
                        send_verification_email(user.email, token)
                        flash("メールアドレスを変更しました。新しいメールに確認リンクを送信しました。", "success")
                    except Exception as exc:
                        logger.exception("Verification email resend failed", error=str(exc), email=email)
                        flash("確認メールの送信に失敗しました。", "warning")
                else:
                    flash("プロフィールを更新しました。", "success")

                if new_password:
                    if not current_password:
                        flash("現在のパスワードを入力してください。", "danger")
                        return render_template("edit_profile.html", user=user)
                    if not user.check_password(current_password):
                        flash("現在のパスワードが正しくありません。", "danger")
                        return render_template("edit_profile.html", user=user)
                    if len(new_password) < 8:
                        flash("新しいパスワードは8文字以上である必要があります。", "danger")
                        return render_template("edit_profile.html", user=user)
                    if new_password != confirm_password:
                        flash("新しいパスワードが一致しません。", "danger")
                        return render_template("edit_profile.html", user=user)
                    user.set_password(new_password)

                db.session.commit()
                session["username"] = user.username
                session["is_verified"] = bool(user.is_verified)
                return redirect(url_for("pages.edit_profile"))

    return render_template("edit_profile.html", user=user)


@bp.route("/logout")
def logout() -> str:
    session.pop("user_id", None)
    session.pop("username", None)
    session.pop("is_admin", None)
    session.pop("is_verified", None)
    flash("ログアウトしました。", "success")
    return redirect(url_for("pages.index"))


    