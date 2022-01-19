from django.urls import path
from .views import QuizView, QuizDetailView, AnswerReadWriteUpdate, AnswerView, QuestionView, ParticipationView, InviteView


urlpatterns = [
    path('quiz/', QuizView.as_view()),
    path('quiz/<int:pk>/', QuizDetailView.as_view()),
    path('answer/', AnswerView.as_view()),
    path('answer/<int:pk>', AnswerReadWriteUpdate.as_view()),
    path('question/', QuestionView.as_view()),
    path('participation/', ParticipationView.as_view()),
    path('invite/<str:email>/<int:quizpk>', InviteView.as_view())
]

