from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models import Lesson, Quiz, Question, UserProgress
import structlog

logger = structlog.get_logger(__name__)

bp = Blueprint("lessons", __name__)


@bp.route("/lessons")
def lesson_list():
    """List semua lessons dari database"""
    lessons = Lesson.query.order_by(Lesson.order_index).all()
    return render_template("lessons/list.html", lessons=lessons)


@bp.route("/lesson/<slug>")
def lesson_detail(slug):
    """Detail lesson berdasarkan slug"""
    lesson = Lesson.query.filter_by(slug=slug).first_or_404()
    return render_template("lessons/detail.html", lesson=lesson)


@bp.route("/quiz/<int:quiz_id>")
def quiz_detail(quiz_id):
    """Detail quiz berdasarkan ID"""
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).order_by(Question.order_index).all()
    return render_template("lessons/quiz.html", quiz=quiz, questions=questions)