import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status

from ..models import FlashcardSet, Flashcard
from ..serializers import FlashcardSetSerializer, FlashcardSerializer

User = get_user_model()


@pytest.fixture(autouse=True)
def force_authenticate(client, user1):
    client.force_authenticate(user=user1)


@pytest.fixture
def frozen_flashcards(user1, user2, set1, set2, set3):
    flashcards = []
    with freeze_time("2021-01-01"):
        flashcards.append(Flashcard.objects.create(owner=user1, flashcard_set=set1, front='question1', back='answer1'))
    with freeze_time("2021-02-02"):
        flashcards.append(Flashcard.objects.create(owner=user1, flashcard_set=set1, front='question2', back='answer2'))
        flashcards.append(Flashcard.objects.create(owner=user1, flashcard_set=set1, front='question3', back='answer3'))
    with freeze_time("2021-02-03"):
        flashcards.append(Flashcard.objects.create(owner=user1, flashcard_set=set1, front='question4', back='answer4'))
    flashcards.append(Flashcard.objects.create(owner=user1, flashcard_set=set1, front='question5', back='answer5'))
    flashcards.append(Flashcard.objects.create(owner=user1, flashcard_set=set2, front='question6', back='answer6'))
    flashcards.append(Flashcard.objects.create(owner=user2, flashcard_set=set3, front='question7', back='answer7'))
    yield flashcards
    for flashcard in flashcards:
        flashcard.delete()


@pytest.mark.django_db
class TestFlashcardSet:

    def test_get_flashcard_sets(self, client, user1, set1, set2):
        sets = FlashcardSet.objects.filter(owner=user1)
        serializer = FlashcardSetSerializer(sets, many=True)
        response = client.get(reverse('flashcard-set-list'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.json() == serializer.data

    def test_create_new_flashcards_set(self, client):
        data = {'name': 'testing'}
        response = client.post(reverse('flashcard-set-list'), data)
        assert response.status_code == status.HTTP_201_CREATED
        assert FlashcardSet.objects.get(pk=response.data['id']) == FlashcardSet.objects.last()

    def test_rename_flashcard_set(self, client, set1):
        data = {'name': 'renamed'}
        url = reverse('flashcard-set-detail', kwargs={'pk': set1.pk})
        response = client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'renamed'

    def test_delete_flashcard_set(self, client, set1):
        url = reverse('flashcard-set-detail', kwargs={'pk': set1.pk})
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestFlashcard:

    def test_get_flashcards(self, client, user1, user2, set1, set2, set3, flashcard_factory):
        flashcard_factory.create_batch(size=3, owner=user1, flashcard_set=set1)
        flashcard_factory.create_batch(size=2, owner=user1, flashcard_set=set2)
        flashcard_factory.create_batch(size=2, owner=user2, flashcard_set=set3)
        response = client.get(reverse('flashcard-list'))
        flashcards = Flashcard.objects.filter(owner=user1)
        serializer = FlashcardSerializer(flashcards, many=True)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 5
        assert response.json() == serializer.data

    def test_create_flashcard(self, client, set1):
        data = {'flashcard_set': set1.pk, 'front': 'question', 'back': 'answer'}
        url = reverse('flashcard-list')
        response = client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Flashcard.objects.get(pk=response.data['id']) == Flashcard.objects.last()

    def test_delete_flashcard(self, client, user1, set1):
        flashcard = Flashcard.objects.create(owner=user1, flashcard_set=set1, front='question',
                                             back='answer')
        url = reverse('flashcard-set-detail', kwargs={'pk': flashcard.pk})
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_edit_front(self, client, user1, set1):
        flashcard = Flashcard.objects.create(owner=user1, flashcard_set=set1, front='question',
                                             back='answer')
        data = {'front': 'question_changed'}
        url = reverse('flashcard-detail', kwargs={'pk': flashcard.pk})
        response = client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['front'] == 'question_changed'

    def test_edit_back(self, client, user1, set1):
        flashcard = Flashcard.objects.create(owner=user1, flashcard_set=set1, front='question',
                                             back='answer')
        data = {'back': 'answer_changed'}
        url = reverse('flashcard-detail', kwargs={'pk': flashcard.pk})
        response = client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['back'] == 'answer_changed'

    def test_search_in_back_and_front(self, client, user1, user2, set1, set2, set3):
        Flashcard.objects.create(owner=user1, flashcard_set=set1, front='palec', back='finger')
        Flashcard.objects.create(owner=user1, flashcard_set=set1, front='płetwa', back='fin')
        Flashcard.objects.create(owner=user1, flashcard_set=set2, front='palce', back='fingers')
        Flashcard.objects.create(owner=user2, flashcard_set=set3, front='finał', back='final')
        response = client.get(reverse('flashcard-list') + '?search=fin')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_search_in_front(self, client, user1, user2, set1, set2, set3):
        Flashcard.objects.create(owner=user1, flashcard_set=set1, front='palec', back='finger')
        Flashcard.objects.create(owner=user1, flashcard_set=set1, front='blady', back='pale')
        Flashcard.objects.create(owner=user1, flashcard_set=set2, front='palce', back='fingers')
        Flashcard.objects.create(owner=user2, flashcard_set=set3, front='palma', back='palm')
        response = client.get(reverse('flashcard-list') + '?search_field=front&search=pal')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_search_in_back(self, client, user1, user2, set1, set2, set3):
        Flashcard.objects.create(owner=user1, flashcard_set=set1, front='palec', back='finger')
        Flashcard.objects.create(owner=user1, flashcard_set=set1, front='blady', back='pale')
        Flashcard.objects.create(owner=user1, flashcard_set=set2, front='palce', back='fingers')
        Flashcard.objects.create(owner=user2, flashcard_set=set3, front='palma', back='palm')
        response = client.get(reverse('flashcard-list') + '?search_field=back&search=pal')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1


@pytest.mark.django_db
class TestFlashcardList:

    def test_get_flashcards(self, client, user1, user2, set1, set2, set3, flashcard_factory):
        flashcard_factory.create_batch(size=5, owner=user1, flashcard_set=set1)
        flashcard_factory.create_batch(size=2, owner=user1, flashcard_set=set2)
        flashcard_factory.create_batch(size=2, owner=user2, flashcard_set=set3)
        url = reverse('list', kwargs={'flashcard_set_pk': set1.pk})
        response = client.get(url)
        flashcards = Flashcard.objects.filter(flashcard_set=set1)
        serializer = FlashcardSerializer(flashcards, many=True)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 5
        assert response.json()['results'] == serializer.data

    def test_create_flashcard_not_allowed(self, client, set1):
        url = reverse('list', kwargs={'flashcard_set_pk': set1.pk})
        data = {'flashcard_set': set1.pk, 'front': 'question', 'back': 'answer'}
        response = client.post(url, data)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_filter_flashcards_with_min_date_only(self, client, set1, frozen_flashcards):
        url = reverse('list', kwargs={'flashcard_set_pk': set1.pk})
        response = client.get(url + '?min_date=2021-02-02')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 4

    def test_filter_flashcards_with_max_date_only(self, client, set1, frozen_flashcards):
        url = reverse('list', kwargs={'flashcard_set_pk': set1.pk})
        response = client.get(url + '?max_date=2021-02-03')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 4

    def test_filter_flashcards_with_both_max_and_min_date(self, client, set1, frozen_flashcards):
        url = reverse('list', kwargs={'flashcard_set_pk': set1.pk})
        response = client.get(url + '?min_date=2021-02-02&max_date=2021-02-03')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3


@pytest.mark.django_db
class TestSearchView:

    def test_search_in_back_and_front(self, client, user1, set1):
        Flashcard.objects.create(owner=user1, flashcard_set=set1, front='palec', back='finger')
        Flashcard.objects.create(owner=user1, flashcard_set=set1, front='płetwa', back='fin')
        Flashcard.objects.create(owner=user1, flashcard_set=set1, front='pytanie', back='question')
        Flashcard.objects.create(owner=user1, flashcard_set=set1, front='finał', back='final')
        url = reverse('search-set', kwargs={'flashcard_set_pk': set1.pk})
        response = client.get(url + '?search=fin')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_search_in_front(self, client, user1, set1):
        Flashcard.objects.create(owner=user1, flashcard_set=set1, front='palec', back='finger')
        Flashcard.objects.create(owner=user1, flashcard_set=set1, front='płetwa', back='fin')
        Flashcard.objects.create(owner=user1, flashcard_set=set1, front='pytanie', back='question')
        Flashcard.objects.create(owner=user1, flashcard_set=set1, front='finał', back='final')
        url = reverse('search-set', kwargs={'flashcard_set_pk': set1.pk})
        response = client.get(url + '?search_field=front&search=fin')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_search_in_back(self, client, user1, set1):
        Flashcard.objects.create(owner=user1, flashcard_set=set1, front='palec', back='finger')
        Flashcard.objects.create(owner=user1, flashcard_set=set1, front='płetwa', back='fin')
        Flashcard.objects.create(owner=user1, flashcard_set=set1, front='pytanie', back='question')
        Flashcard.objects.create(owner=user1, flashcard_set=set1, front='finał', back='final')
        url = reverse('search-set', kwargs={'flashcard_set_pk': set1.pk})
        response = client.get(url + '?search_field=back&search=quest')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
