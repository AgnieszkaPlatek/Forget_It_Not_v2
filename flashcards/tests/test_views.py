from django.contrib.auth import get_user_model
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from ..models import FlashcardSet, Flashcard
from ..serializers import FlashcardSetSerializer, FlashcardSerializer

User = get_user_model()


class FlashcardSetTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='Tester1')
        self.client.force_authenticate(user=self.user)

    def test_get_flashcard_sets(self):
        FlashcardSet.objects.create(name='set1', owner=self.user)
        FlashcardSet.objects.create(name='set2', owner=self.user)
        sets = FlashcardSet.objects.filter(owner=self.user)
        serializer = FlashcardSetSerializer(sets, many=True)
        response = self.client.get(reverse('flashcard-set-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.json(), serializer.data)

    def test_create_new_flashcards_set(self):
        data = {'name': 'testing'}
        response = self.client.post(reverse('flashcard-set-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FlashcardSet.objects.get(pk=response.data['id']), FlashcardSet.objects.last())

    def test_rename_flashcard_set(self):
        set1 = FlashcardSet.objects.create(name='set1', owner=self.user)
        data = {'name': 'renamed'}
        url = reverse('flashcard-set-detail', kwargs={'pk': set1.pk})
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'renamed')

    def test_delete_flashcard_set(self):
        set1 = FlashcardSet.objects.create(name='set1', owner=self.user)
        url = reverse('flashcard-set-detail', kwargs={'pk': set1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class FlashcardTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create(username='Tester1')
        self.user2 = User.objects.create(username='Tester2')
        self.client.force_authenticate(user=self.user1)
        self.set1 = FlashcardSet.objects.create(name='set1', owner=self.user1)
        self.set2 = FlashcardSet.objects.create(name='set2', owner=self.user1)
        self.set3 = FlashcardSet.objects.create(name='set3', owner=self.user2)

    def test_get_flashcards(self):
        Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question1', back='answer1')
        Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question2', back='answer2')
        Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question3', back='answer3')
        Flashcard.objects.create(owner=self.user1, flashcard_set=self.set2, front='question4', back='answer4')
        Flashcard.objects.create(owner=self.user2, flashcard_set=self.set3, front='question5', back='answer5')
        response = self.client.get(reverse('flashcard-list'))
        flashcards = Flashcard.objects.filter(owner=self.user1)
        serializer = FlashcardSerializer(flashcards, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.json(), serializer.data)

    def test_create_flashcard(self):
        data = {'flashcard_set': self.set1.pk, 'front': 'question', 'back': 'answer'}
        url = reverse('flashcard-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Flashcard.objects.get(pk=response.data['id']), Flashcard.objects.last())

    def test_delete_flashcard(self):
        flashcard = Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question',
                                             back='answer')
        url = reverse('flashcard-set-detail', kwargs={'pk': flashcard.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_edit_front(self):
        flashcard = Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question',
                                             back='answer')
        data = {'front': 'question_changed'}
        url = reverse('flashcard-detail', kwargs={'pk': flashcard.pk})
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['front'], 'question_changed')

    def test_edit_back(self):
        flashcard = Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question',
                                             back='answer')
        data = {'back': 'answer_changed'}
        url = reverse('flashcard-detail', kwargs={'pk': flashcard.pk})
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['back'], 'answer_changed')


class FlashcardListTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create(username='Tester1')
        self.user2 = User.objects.create(username='Tester2')
        self.client.force_authenticate(user=self.user1)
        self.set1 = FlashcardSet.objects.create(name='set1', owner=self.user1)
        self.set2 = FlashcardSet.objects.create(name='set2', owner=self.user1)
        self.set3 = FlashcardSet.objects.create(name='set3', owner=self.user2)
        self.url = reverse('list', kwargs={'flashcard_set_pk': self.set1.pk})
        with freeze_time("2021-01-01"):
            Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question1', back='answer1')
        with freeze_time("2021-02-02"):
            Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question2', back='answer2')
            Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question3', back='answer3')
        with freeze_time("2021-02-03"):
            Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question4', back='answer4')
        Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question5', back='answer5')
        Flashcard.objects.create(owner=self.user1, flashcard_set=self.set2, front='question6', back='answer6')
        Flashcard.objects.create(owner=self.user2, flashcard_set=self.set3, front='question7', back='answer7')

    def test_get_flashcards(self):
        response = self.client.get(self.url)
        flashcards = Flashcard.objects.filter(flashcard_set=self.set1)
        serializer = FlashcardSerializer(flashcards, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        self.assertEqual(response.json()['results'], serializer.data)

    def test_create_flashcard_not_allowed(self):
        data = {'flashcard_set': self.set1.pk, 'front': 'question', 'back': 'answer'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_filter_flashcards_with_min_date_only(self):
        response = self.client.get(self.url + '?min_date=2021-02-02')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 4)

    def test_filter_flashcards_with_max_date_only(self):
        response = self.client.get(self.url + '?max_date=2021-02-03')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 4)

    def test_filter_flashcards_with_both_max_and_min_date(self):
        response = self.client.get(self.url + '?min_date=2021-02-02&max_date=2021-02-03')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)


class SearchView(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create(username='Tester1')
        self.client.force_authenticate(user=self.user1)
        self.set1 = FlashcardSet.objects.create(name='set1', owner=self.user1)
        self.url = reverse('search-set', kwargs={'flashcard_set_pk': self.set1.pk})
        Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='palec', back='finger')
        Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='płetwa', back='fin')
        Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='pytanie', back='question')
        Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='finał', back='final')

    def test_search_in_back_and_front(self):
        response = self.client.get(self.url + '?search=fin')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_search_in_front(self):
        response = self.client.get(self.url + '?search_fields=front&search=fin')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_in_both(self):
        response = self.client.get(self.url + '?search_fields=back&search=quest')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
