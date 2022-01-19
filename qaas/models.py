from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    isCorrect = models.BooleanField()

    def __str__(self):
        return f"{self.question} {str(self.text)} {self.isCorrect}"


class Participation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} {self.quiz.name}"


class AnswersGiven(models.Model):
    participation = models.ForeignKey(Participation, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selectedAnswer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.participation) + " " + str(self.question) + " " + str(self.selectedAnswer)
