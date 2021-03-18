from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status

from ..models import FlashcardSet, Flashcard
from ..serializers import FlashcardSetSerializer


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


class FlashcardTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        user = User.objects.create(username='Tester1')
        self.client.force_authenticate(user=user)
        self.set1 = FlashcardSet.objects.create(name='set1', owner=user)
        self.url = reverse('flashcard-list')

    def test_get_flashcards(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_flashcard(self):
        data = {'flashcard_set': self.set1.pk, 'front': 'question', 'back': 'answer'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class FlashcardListTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        user = User.objects.create(username='Tester1')
        self.client.force_authenticate(user=user)
        self.set1 = FlashcardSet.objects.create(name='set1', owner=user)
        set1 = FlashcardSet.objects.create(name='set1', owner=user)
        self.set1_pk = set1.pk
        self.url = reverse('user-list', kwargs={'flashcard_set_pk': self.set1_pk})

    def test_get_flashcards(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_flashcard_not_allowed(self):
        data = {'flashcard_set': self.set1_pk, 'front': 'question', 'back': 'answer'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class FlashcardLearnView(APITestCase):
    pass


class SearchView(APITestCase):
    pass