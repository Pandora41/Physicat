from app import create_app, db
from app.config import Settings
from sqlalchemy import text

settings = Settings(
    flask_env="development",
    flask_debug=False,
    database_url="sqlite:///app.db",
    secret_key="dev-secret-key-change-in-production",
)

app = create_app(settings)

with app.app_context():
    result = db.session.execute(text("PRAGMA table_info(lessons)"))
    columns = [row[1] for row in result]
    print("existing columns:", columns)

    if "simulation_type" in columns:
        db.session.execute(text("ALTER TABLE lessons DROP COLUMN simulation_type"))
        db.session.commit()
        print("dropped simulation_type")
    else:
        print("simulation_type already absent")
