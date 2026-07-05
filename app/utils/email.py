import smtplib
from email.message import EmailMessage
from itsdangerous import URLSafeTimedSerializer

from app.config import get_settings


def _get_serializer() -> URLSafeTimedSerializer:
    settings = get_settings()
    return URLSafeTimedSerializer(settings.secret_key, salt="email-verify")


def generate_verification_token(email: str) -> str:
    serializer = _get_serializer()
    return serializer.dumps(email)


def confirm_verification_token(token: str, expiration: int = 3600) -> str:
    serializer = _get_serializer()
    return serializer.loads(token, max_age=expiration)


def send_verification_email(recipient: str, token: str) -> None:
    settings = get_settings()
    if not settings.mail_server or not settings.mail_username or not settings.mail_password:
        # If mail is not configured, skip sending and rely on console logging.
        print(f"[email] verification token for {recipient}: {token}")
        return

    verify_url = f"http://localhost:5000/verify/{token}"
    message = EmailMessage()
    message["Subject"] = "Physicatメール確認"
    message["From"] = settings.mail_default_sender
    message["To"] = recipient
    message.set_content(
        f"Physicatへようこそ！\n\n以下のリンクをクリックしてメールアドレスを確認してください:\n{verify_url}\n\nこのリンクは1時間有効です。"
    )

    if settings.mail_use_ssl:
        smtp_class = smtplib.SMTP_SSL
    else:
        smtp_class = smtplib.SMTP

    with smtp_class(settings.mail_server, settings.mail_port) as smtp:
        if settings.mail_use_tls and not settings.mail_use_ssl:
            smtp.starttls()
        smtp.login(settings.mail_username, settings.mail_password)
        smtp.send_message(message)
