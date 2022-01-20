from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse


class QuizCreationTest(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'testingcreatorone@mail.com',
            'testingCreatorOne'
        )
        self.client.force_authenticate(self.user)

    def test_create_brand_new_quiz(self):
        url = reverse('create-quiz')
        res = self.client.post(url, {'name': 'A new quiz to test'}, format='json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['creator'], 1)

    def test_add_question_to_quiz(self):
        # create the quizs
        quizs = self.client.get(reverse('my-quizs'), format='json')
        self.assertEqual(len(quizs.data), 0)

        created = self.client.post(reverse('create-quiz'), {'name': 'TestExistingQuiz'}, format='json')
        res = self.client.post('/qaas/question/new/1', {'text': 'Can you add questions by an api'}, format='json')
        self.assertEqual(res.data['quiz'], created.data['id'])

        quizs = self.client.get(reverse('my-quizs'), format='json')
        self.assertEqual(len(quizs.data), 1)

    def test_update_question_from_quiz(self):
        text_to_update = 'Can you CHANGE text of questio per api'
        self.client.post(reverse('create-quiz'), {'name': 'TestExistingQuiz'}, format='json')
        self.client.post('/qaas/question/new/1', {'text': 'Can you add questions by an api'}, format='json')

        res = self.client.put('/qaas/question/update/1', {'text': text_to_update}, format='json')
        self.assertEqual(res.data['text'], text_to_update)

    def test_delete_question_from_quiz(self):
        res = self.client.post(reverse('create-quiz'), {'name': 'TestExistingQuiz'}, format='json')
        self.client.post('/qaas/question/new/1', {'text': 'Can you add questions by an api'}, format='json')

        self.client.delete('/qaas/question/update/1')

        #check that quiz has 0 answers
        res = self.client.get(reverse('my-quizs'))
        self.assertEqual(len(res.data[0]['questions']), 0)

    def test_add_answer_to_quiz(self):
        pass