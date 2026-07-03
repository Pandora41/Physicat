from app.extensions import db
from datetime import datetime
import enum

# Enums buat validasi
class CategoryEnum(enum.Enum):
    GELOMBANG = "Gelombang"
    MEKANIKA = "Mekanika"
    QUANTUM = "Quantum"
    THERMODYNAMICS = "Thermodynamics"
    OPTICS = "Optics"

class SimulationTypeEnum(enum.Enum):
    WAVE = "wave"
    PROJECTILE = "projectile"
    BB84 = "bb84"

class Lesson(db.Model):
    __tablename__ = "lessons"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    category = db.Column(
        db.Enum(
            CategoryEnum,
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
            native_enum=False,
        ),
        default=CategoryEnum.MEKANIKA,
    )
    description = db.Column(db.Text, nullable=True)
    content_html = db.Column(db.Text, nullable=True)
    simulation_type = db.Column(
        db.Enum(
            SimulationTypeEnum,
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
            native_enum=False,
        ),
        nullable=True,
    )
    order_index = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    quizzes = db.relationship("Quiz", back_populates="lesson", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Lesson {self.title}>"