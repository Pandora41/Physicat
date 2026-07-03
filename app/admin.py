from sqladmin import Admin, ModelView
from app.extensions import db
from app.models import User, Lesson, Quiz, Question, UserProgress

def setup_admin(app):
    # Initialize SQLAdmin dashboard with the Flask app and database object
    admin = Admin(app, db, base_url="/admin")
    
    # User Admin
    class UserAdmin(ModelView, model=User):
        column_list = [User.id, User.username, User.email, User.is_admin, User.created_at]
        column_searchable_list = [User.username, User.email]
        column_sortable_list = [User.id, User.username, User.created_at]
        column_default_sort = (User.created_at, True)
        form_excluded_columns = [User.password_hash, User.created_at, User.progress]
        
    # Lesson Admin
    class LessonAdmin(ModelView, model=Lesson):
        column_list = [Lesson.id, Lesson.title, Lesson.slug, Lesson.category, Lesson.simulation_type, Lesson.order_index]
        column_searchable_list = [Lesson.title, Lesson.slug]
        column_sortable_list = [Lesson.id, Lesson.title, Lesson.order_index]
        column_default_sort = (Lesson.order_index, False)
        form_excluded_columns = [Lesson.created_at, Lesson.updated_at, Lesson.quizzes]
        
    # Quiz Admin
    class QuizAdmin(ModelView, model=Quiz):
        column_list = [Quiz.id, Quiz.title, Quiz.lesson, Quiz.created_at]
        column_searchable_list = [Quiz.title]
        column_sortable_list = [Quiz.id, Quiz.title, Quiz.created_at]
        column_default_sort = (Quiz.created_at, True)
        form_excluded_columns = [Quiz.created_at, Quiz.questions]
        
    # Question Admin
    class QuestionAdmin(ModelView, model=Question):
        column_list = [Question.id, Question.quiz, Question.question_text, Question.correct_answer, Question.order_index]
        column_searchable_list = [Question.question_text]
        column_sortable_list = [Question.id, Question.order_index]
        column_default_sort = (Question.order_index, False)
        form_excluded_columns = [Question.created_at]
        form_widget_args = {
            'question_text': {'rows': 3},
            'explanation': {'rows': 3},
        }
        
    # UserProgress Admin
    class UserProgressAdmin(ModelView, model=UserProgress):
        column_list = [UserProgress.id, UserProgress.user, UserProgress.lesson, UserProgress.quiz, UserProgress.score, UserProgress.completed]
        column_sortable_list = [UserProgress.id, UserProgress.score, UserProgress.completed]
        column_default_sort = (UserProgress.id, True)
        form_excluded_columns = [UserProgress.completed_at]
    
    # Add views
    admin.add_view(UserAdmin)
    admin.add_view(LessonAdmin)
    admin.add_view(QuizAdmin)
    admin.add_view(QuestionAdmin)
    admin.add_view(UserProgressAdmin)
    
    return admin