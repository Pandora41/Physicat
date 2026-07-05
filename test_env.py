from app.config import get_settings

settings = get_settings()

print("="*60)
print("🔍 KONFIGURASI DARI .env:")
print("="*60)
print(f"FLASK_ENV:       {settings.flask_env}")
print(f"DATABASE_URL:    {settings.database_url}")
print(f"MAIL_SERVER:     {settings.mail_server}")
print(f"MAIL_PORT:       {settings.mail_port}")
print(f"MAIL_USERNAME:   {settings.mail_username}")
print(f"MAIL_PASSWORD:   {settings.mail_password[:4]}...")
print(f"MAIL_TLS:        {settings.mail_use_tls}")
print(f"MAIL_SENDER:     {settings.mail_default_sender}")
print("="*60)