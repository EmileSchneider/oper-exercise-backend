from django.urls import path
from .views import QuizView, QuizDetailView, AnswerReadWriteUpdate, AnswerView, QuestionView, ParticipationView, InviteView
from .views import QuizCreateView, QuestionCreateView, QuestionUpdateView

urlpatterns = [
    path('quiz/', QuizView.as_view(), name='my-quizs'),
    path('quiz/<int:pk>/', QuizDetailView.as_view()),
    path('quiz/new/', QuizCreateView.as_view(), name='create-quiz'),
    path('answer/', AnswerView.as_view()),
    path('answer/<int:pk>', AnswerReadWriteUpdate.as_view()),
    path('question/', QuestionView.as_view()),
    path('question/new/<int:quizid>', QuestionCreateView.as_view(), name='add'),
    path('question/update/<int:questionid>', QuestionUpdateView.as_view(), name='update-question'),
    path('participation/', ParticipationView.as_view()),
    path('invite/<str:email>/<int:quizpk>', InviteView.as_view())
]

