from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from users.models import User
from ..models import FlashcardSet, Flashcard
from ..views import FlashcardViewSet, FlashcardSetViewSet, FlashcardListView


class FlashcardSetTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username='Tester1')
        self.endpoint = '/flashcard-sets/'

    def test_get_flashcard_sets(self):
        request = self.factory.get(self.endpoint)
        force_authenticate(request, user=self.user)
        response = FlashcardSetViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(200, response.status_code)

    def test_create_new_flashcards_set(self):
        data = {'name': 'testing'}
        request = self.factory.post(self.endpoint, data)
        force_authenticate(request, user=self.user)
        response = FlashcardSetViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(201, response.status_code)


class FlashcardTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username='Tester1')
        self.set1 = FlashcardSet.objects.create(name='set1', owner=self.user)
        self.endpoint = '/flashcards/'

    def test_get_flashcards(self):
        request = self.factory.get(self.endpoint)
        force_authenticate(request, user=self.user)
        response = FlashcardViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(200, response.status_code)

    def test_create_flashcard(self):
        data = {'flashcard_set': self.set1.pk, 'front': 'question', 'back': 'answer'}
        request = self.factory.post(self.endpoint, data)
        force_authenticate(request, user=self.user)
        response = FlashcardViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(201, response.status_code)


class FlashcardListTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username='Tester1')
        set1 = FlashcardSet.objects.create(name='set1', owner=self.user)
        self.set1_pk = set1.pk
        self.endpoint = '/flashcard-list/' + str(self.set1_pk)

    def test_get_flashcards(self):
        request = self.factory.get(self.endpoint)
        force_authenticate(request, user=self.user)
        response = FlashcardListView.as_view()(request)
        self.assertEqual(200, response.status_code)

    def test_create_flashcard_not_allowed(self):
        data = {'flashcard_set': self.set1_pk, 'front': 'question', 'back': 'answer'}
        request = self.factory.post(self.endpoint, data)
        force_authenticate(request, user=self.user)
        response = FlashcardListView.as_view()(request)
        self.assertEqual(405, response.status_code)
