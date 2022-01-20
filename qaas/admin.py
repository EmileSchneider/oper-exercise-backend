from django.contrib import admin

from .models import Quiz, Question, Answer, AnswersGiven, Participation

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(AnswersGiven)
admin.site.register(Participation)