from app.extensions import db
from datetime import datetime

class UserProgress(db.Model):
    __tablename__ = "user_progress"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lessons.id"), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"), nullable=True)
    score = db.Column(db.Float, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    user = db.relationship("User", back_populates="progress")
    lesson = db.relationship("Lesson")
    quiz = db.relationship("Quiz")
    
    def __repr__(self):
        return f"<UserProgress user={self.user_id} lesson={self.lesson_id}>"