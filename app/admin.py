try:
    from flask_admin import Admin
    from flask_admin.contrib.sqla import ModelView
except ImportError:  # pragma: no cover
    Admin = None
    ModelView = None

from app.extensions import db
from app.models import User, Lesson, Quiz, Question, UserProgress


class UserAdmin(ModelView):
    column_list = ["id", "username", "email", "is_admin", "created_at"]
    column_searchable_list = ["username", "email"]
    column_sortable_list = ["id", "username", "created_at"]
    column_default_sort = ("created_at", True)
    form_excluded_columns = ["password_hash", "progress"]


class LessonAdmin(ModelView):
    column_list = ["id", "title", "slug", "category", "simulation_type", "order_index"]
    column_searchable_list = ["title", "slug"]
    column_sortable_list = ["id", "title", "order_index"]
    column_default_sort = ("order_index", False)
    form_excluded_columns = ["created_at", "updated_at", "quizzes"]


class QuizAdmin(ModelView):
    column_list = ["id", "title", "lesson", "created_at"]
    column_searchable_list = ["title"]
    column_sortable_list = ["id", "title", "created_at"]
    column_default_sort = ("created_at", True)
    form_excluded_columns = ["created_at", "questions"]


class QuestionAdmin(ModelView):
    column_list = ["id", "quiz", "question_text", "correct_answer", "order_index"]
    column_searchable_list = ["question_text"]
    column_sortable_list = ["id", "order_index"]
    column_default_sort = ("order_index", False)
    form_excluded_columns = ["created_at"]
    form_widget_args = {
        "question_text": {"rows": 3},
        "explanation": {"rows": 3},
    }


class UserProgressAdmin(ModelView):
    column_list = ["id", "user", "lesson", "quiz", "score", "completed"]
    column_sortable_list = ["id", "score", "completed"]
    column_default_sort = ("id", True)
    form_excluded_columns = ["completed_at"]


def setup_admin(app):
    if Admin is None or ModelView is None:
        return None

    admin = Admin(app, name="Physicat Admin", url="/admin")
    admin.add_view(UserAdmin(User, db.session, name="Users"))
    admin.add_view(LessonAdmin(Lesson, db.session, name="Lessons"))
    admin.add_view(QuizAdmin(Quiz, db.session, name="Quizzes"))
    admin.add_view(QuestionAdmin(Question, db.session, name="Questions"))
    admin.add_view(UserProgressAdmin(UserProgress, db.session, name="Progress"))

    return admin
