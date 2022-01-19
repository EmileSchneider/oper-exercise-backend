from rest_framework import generics
from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated

from .models import Quiz, Answer, Question, Participation, Invitation
from .serialisers import QuizSerialiser, AnswerSerialiser, QuestionSerialiser, ParticipationSerialiser

from invitations.utils import get_invitation_model


class InviteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, email, quizpk):
        inv = get_invitation_model()
        invite = inv.create(email, inviter=request.user)
        invite.send_invitation(request)
        i = Invitation(email=email, quiz=quizpk)
        i.save()
        return Response({})


class ParticipationView(generics.ListAPIView):
    serializer_class = ParticipationSerialiser
    queryset = Participation.objects.all()


class QuizView(APIView):

    def get(self, request):
        quizs = Quiz.objects.all()
        serialiser = QuizSerialiser(quizs, many=True)
        return Response(serialiser.data)


class QuizDetailView(APIView):

    def get(self, request, pk):
        quiz = Quiz.objects.get(pk=pk)
        serialiser = QuizSerialiser(quiz)
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
