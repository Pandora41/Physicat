from app.extensions import db
from datetime import datetime
import enum

# Enums buat validasi
class CategoryEnum(enum.Enum):
    WAVE = "波動"
    MECHANICS = "力学"
    QUANTUM = "量子"
    THERMODYNAMICS = "熱力学"
    OPTICS = "光学"

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
        default=CategoryEnum.MECHANICS,
    )
    description = db.Column(db.Text, nullable=True)
    content_html = db.Column(db.Text, nullable=True)
    order_index = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    quizzes = db.relationship("Quiz", back_populates="lesson", cascade="all, delete-orphan")

    def get_category_label(self) -> str:
        if not self.category:
            return "一般"

        mapping = {
            "Wave": "波動",
            "Mechanics": "力学",
            "Quantum": "量子",
            "Thermodynamics": "熱力学",
            "Optics": "光学",
            "波動": "波動",
            "力学": "力学",
            "量子": "量子",
            "熱力学": "熱力学",
            "光学": "光学",
        }
        return mapping.get(self.category.value, self.category.value)
    
    def __repr__(self):
        return f"<Lesson {self.title}>"