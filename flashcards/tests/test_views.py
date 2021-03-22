from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status

from ..models import FlashcardSet, Flashcard
from ..serializers import FlashcardSetSerializer, FlashcardSerializer


User = get_user_model()


class FlashcardSetTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='Tester1')
        self.client.force_authenticate(user=self.user)
        self.url = (reverse('flashcard-set-list'))

    def test_get_flashcard_sets(self):
        FlashcardSet.objects.create(name='set1', owner=self.user)
        FlashcardSet.objects.create(name='set2', owner=self.user)
        sets = FlashcardSet.objects.filter(owner=self.user)
        serializer = FlashcardSetSerializer(sets, many=True)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.json(), serializer.data)

    def test_create_new_flashcards_set(self):
        data = {'name': 'testing'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FlashcardSet.objects.get(pk=response.data['id']), FlashcardSet.objects.last())


class FlashcardTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create(username='Tester1')
        self.user2 = User.objects.create(username='Tester2')
        self.client.force_authenticate(user=self.user1)
        self.set1 = FlashcardSet.objects.create(name='set1', owner=self.user1)
        self.set2 = FlashcardSet.objects.create(name='set2', owner=self.user1)
        self.set3 = FlashcardSet.objects.create(name='set3', owner=self.user2)
        self.url = reverse('flashcard-list')

    def test_get_flashcards(self):
        Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question1', back='answer1')
        Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question2', back='answer2')
        Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question3', back='answer3')
        Flashcard.objects.create(owner=self.user1, flashcard_set=self.set2, front='question4', back='answer4')
        Flashcard.objects.create(owner=self.user2, flashcard_set=self.set3, front='question5', back='answer5')
        response = self.client.get(self.url)
        flashcards = Flashcard.objects.filter(owner=self.user1)
        serializer = FlashcardSerializer(flashcards, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.json(), serializer.data)

    def test_create_flashcard(self):
        data = {'flashcard_set': self.set1.pk, 'front': 'question', 'back': 'answer'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Flashcard.objects.get(pk=response.data['id']), Flashcard.objects.last())


class FlashcardListTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create(username='Tester1')
        self.user2 = User.objects.create(username='Tester2')
        self.client.force_authenticate(user=self.user1)
        self.set1 = FlashcardSet.objects.create(name='set1', owner=self.user1)
        self.set2 = FlashcardSet.objects.create(name='set2', owner=self.user1)
        self.set3 = FlashcardSet.objects.create(name='set3', owner=self.user2)
        Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question1', back='answer1')
        Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question2', back='answer2')
        Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question3', back='answer3')
        Flashcard.objects.create(owner=self.user1, flashcard_set=self.set2, front='question4', back='answer4')
        Flashcard.objects.create(owner=self.user2, flashcard_set=self.set3, front='question5', back='answer5')
        self.url = reverse('list', kwargs={'flashcard_set_pk': self.set1.pk})

    def test_get_flashcards(self):
        response = self.client.get(self.url)
        flashcards = Flashcard.objects.filter(flashcard_set=self.set1)
        serializer = FlashcardSerializer(flashcards, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.json()['results'], serializer.data)

    def test_create_flashcard_not_allowed(self):
        data = {'flashcard_set': self.set1.pk, 'front': 'question', 'back': 'answer'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class FlashcardLearnView(APITestCase):
    pass


class SearchView(APITestCase):
    pass
