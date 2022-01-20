import http

from rest_framework import generics, mixins
from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User

from .models import Quiz, Answer, Question, Participation, QuizInvitations
from .serialisers import QuizSerialiser, DetailedQuizSerialiser, AnswerSerialiser, QuestionSerialiser, \
    ParticipationSerialiser

from invitations.utils import get_invitation_model

from django.core.mail import send_mail
import oper.settings as settings


class InviteView(APIView):
    permission_classes = [IsAuthenticated]

    def __invite_to_quiz__(self, email, quizpk):
        qi = QuizInvitations(email=email, quiz=Quiz.objects.get(pk=quizpk))
        qi.save()
        send_mail(
            f'Invited to participated in Quiz: {Quiz.objects.get(pk=quizpk).name}',
            'Log into your account and do the quiz',
            settings.SERVER_EMAIL,
            [email],
            fail_silently=False,
        )

    def get(self, request, email, quizpk):
        try:
            User.objects.get(email=email)
            self.__invite_to_quiz__(email, quizpk)
        except User.DoesNotExist:
            inv = get_invitation_model()
            invite = inv.create(email, inviter=request.user)
            invite.send_invitation(request)
            self.__invite_to_quiz__(email, quizpk)
        return Response({})


class ParticipationView(generics.ListAPIView):
    serializer_class = ParticipationSerialiser
    queryset = Participation.objects.all()


class QuizView(APIView):

    def get(self, request):
        user = User.objects.get(username=request.user)
        quizs = Quiz.objects.filter(creator=user.pk)
        serialiser = DetailedQuizSerialiser(quizs, many=True)
        return Response(serialiser.data)


class QuizCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = User.objects.get(username=request.user)
        data = {**request.data, 'creator': user.pk}
        quizserialiser = QuizSerialiser(data=data, context={'request': request})

        if quizserialiser.is_valid():
            obj = quizserialiser.save()
            return Response({**quizserialiser.data, 'id': obj.id}, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class QuizDetailView(APIView):

    def get(self, request, pk):
        quiz = Quiz.objects.get(pk=pk)
        serialiser = DetailedQuizSerialiser(quiz)
        return Response(serialiser.data)


class AnswerView(generics.ListAPIView):
    serializer_class = AnswerSerialiser
    queryset = Answer.objects.all()


class AnswerReadWriteUpdate(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnswerSerialiser
    queryset = Answer.objects.all()


class QuestionView(generics.ListCreateAPIView):
    serializer_class = QuestionSerialiser
    queryset = Question.objects.all()


class QuestionCreateView(APIView):

    def post(self, request, quizid):
        try:
            quiz = Quiz.objects.get(pk=quizid)
            data = {**request.data, 'quiz': quizid}
            questionserializer = QuestionSerialiser(data=data)
            if questionserializer.is_valid():
                questionserializer.save()
                return Response(data=questionserializer.data, status=status.HTTP_201_CREATED)
            return Response(data="data invalid", status=status.HTTP_400_BAD_REQUEST)

        except Quiz.DoesNotExist:
            return Response(data="quiz does not exist", status=status.HTTP_400_BAD_REQUEST)


class QuestionUpdateView(APIView):

    def put(self, request, questionid):
        try:
            question = Question.objects.get(pk=questionid)
            q = Question(id=questionid, text=request.data['text'], quiz=question.quiz)
            q.save()
            return Response(data=QuestionSerialiser(q).data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, questionid):
        try:
            Question.objects.filter(id=questionid).delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
