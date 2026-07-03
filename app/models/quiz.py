from app.extensions import db
from datetime import datetime

class Quiz(db.Model):
    __tablename__ = "quizzes"
    
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lessons.id"), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    lesson = db.relationship("Lesson", back_populates="quizzes")
    questions = db.relationship("Question", back_populates="quiz", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Quiz {self.title}>"


class Question(db.Model):
    __tablename__ = "questions"
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    options = db.Column(db.JSON, nullable=False)  # ["Opsi A", "Opsi B", "Opsi C", "Opsi D"]
    correct_answer = db.Column(db.Integer, nullable=False)  # Index 0-3
    explanation = db.Column(db.Text, nullable=True)
    order_index = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    quiz = db.relationship("Quiz", back_populates="questions")
    
    def __repr__(self):
        return f"<Question {self.id}>"