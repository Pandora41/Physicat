import sys
import os

# Tambahin folder root project ke Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Ensure database tables exist before querying
    db.create_all()

    # Check kalau admin udah ada
    admin = User.query.filter_by(username="admin").first()
    
    if admin:
        print("Admin user already exists!")
    else:
        # Bikin admin user
        admin = User(
            username="admin",
            email="admin@physicat.com",
            is_admin=True,
            is_verified=True
        )
        admin.set_password("admin123")  # GANTI PASSWORD INI!
        
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully!")
        print("Username: admin")
        print("Password: admin123")