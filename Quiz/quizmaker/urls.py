from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),

    # API Routes
    path('quiz/<int:quiz_id>', views.quiz, name='quiz'),
    path('score/<str:category>/<int:quiz_id>', views.score, name='score'),
    path('remove_quiz/<int:quiz_id>', views.remove_quiz, name='remove_quiz'),
    path('quizzes/<str:category>', views.quizzes, name='quizzes'),
    path('question/<int:question_id>', views.question, name='question'),
    path('remove_question/<int:question_id>', views.remove_question, name='remove_question'),
]
