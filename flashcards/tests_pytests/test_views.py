import pytest
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status

from ..models import FlashcardSet, Flashcard
from ..serializers import FlashcardSetSerializer, FlashcardSerializer


@pytest.mark.django_db
class TestFlashcardSet:

    def test_get_flashcard_sets(self, api_client, user, flashcard_set_factory):
        flashcard_sets = flashcard_set_factory.create_batch(size=2, owner=user)
        serializer = FlashcardSetSerializer(flashcard_sets, many=True)
        api_client.force_authenticate(user=user)

        response = api_client.get(reverse('flashcard-set-list'))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.json() == serializer.data

    def test_create_new_flashcards_set(self, api_client, user):
        data = {'name': 'testing'}
        api_client.force_authenticate(user=user)

        response = api_client.post(reverse('flashcard-set-list'), data)

        assert response.status_code == status.HTTP_201_CREATED
        assert FlashcardSet.objects.get(pk=response.data['id']) == FlashcardSet.objects.last()

    def test_rename_flashcard_set(self, api_client, user, flashcard_set_factory):
        flashcard_set = flashcard_set_factory(owner=user, name='old_name')
        data = {'name': 'renamed'}
        url = reverse('flashcard-set-detail', kwargs={'pk': flashcard_set.pk})
        api_client.force_authenticate(user=user)

        response = api_client.patch(url, data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'renamed'

    def test_delete_flashcard_set(self, api_client, user, flashcard_set_factory):
        flashcard_set = flashcard_set_factory(owner=user)
        url = reverse('flashcard-set-detail', kwargs={'pk': flashcard_set.pk})
        api_client.force_authenticate(user=user)

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestFlashcard:

    def test_get_flashcards(self, api_client, user_factory, flashcard_set_factory, flashcard_factory):
        user1 = user_factory(username='User1')
        user2 = user_factory(username='User2')
        flashcard_set1 = flashcard_set_factory(owner=user1)
        flashcard_set2 = flashcard_set_factory(owner=user1)
        flashcard_set3 = flashcard_set_factory(owner=user2)
        flashcard_factory.create_batch(size=3, owner=user1, flashcard_set=flashcard_set1)
        flashcard_factory.create_batch(size=2, owner=user1, flashcard_set=flashcard_set2)
        flashcard_factory.create_batch(size=2, owner=user2, flashcard_set=flashcard_set3)
        flashcards = Flashcard.objects.filter(owner=user1)
        serializer = FlashcardSerializer(flashcards, many=True)
        api_client.force_authenticate(user=user1)

        response = api_client.get(reverse('flashcard-list'))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 5
        assert response.json() == serializer.data

    def test_create_flashcard(self, api_client, user, flashcard_set_factory):
        flashcard_set = flashcard_set_factory(owner=user)
        data = {'flashcard_set': flashcard_set.pk, 'front': 'question', 'back': 'answer'}
        api_client.force_authenticate(user=user)

        response = api_client.post(reverse('flashcard-list'), data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Flashcard.objects.get(pk=response.data['id']) == Flashcard.objects.last()

    def test_delete_flashcard(self, api_client, user, flashcard_set_factory, flashcard_factory):
        flashcard_set = flashcard_set_factory(owner=user)
        flashcard = flashcard_factory(owner=user, flashcard_set=flashcard_set)
        url = reverse('flashcard-set-detail', kwargs={'pk': flashcard.pk})
        api_client.force_authenticate(user=user)

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_edit_front(self, api_client, user, flashcard_set_factory, flashcard_factory):
        flashcard_set = flashcard_set_factory(owner=user)
        flashcard = flashcard_factory(owner=user, flashcard_set=flashcard_set, front='question', back='answer')
        data = {'front': 'question_changed'}
        url = reverse('flashcard-detail', kwargs={'pk': flashcard.pk})
        api_client.force_authenticate(user=user)

        response = api_client.patch(url, data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['front'] == 'question_changed'

    def test_edit_back(self, api_client, user, flashcard_set_factory, flashcard_factory):
        flashcard_set = flashcard_set_factory(owner=user)
        flashcard = flashcard_factory(owner=user, flashcard_set=flashcard_set, front='question', back='answer')
        data = {'back': 'answer_changed'}
        url = reverse('flashcard-detail', kwargs={'pk': flashcard.pk})
        api_client.force_authenticate(user=user)

        response = api_client.patch(url, data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['back'] == 'answer_changed'

    @pytest.mark.parametrize('query, expected_result', [
        ('?search=pal', 3),
        ('?search_field=front&search=pal', 2),
        ('?search_field=back&search=pal', 1)])
    def test_search(self, query, expected_result, api_client, user_factory, flashcard_set_factory, flashcard_factory):
        user1 = user_factory(username='User1')
        user2 = user_factory(username='User2')
        flashcard_set1 = flashcard_set_factory(owner=user1)
        flashcard_set2 = flashcard_set_factory(owner=user1)
        flashcard_set3 = flashcard_set_factory(owner=user2)
        flashcard_factory(owner=user1, flashcard_set=flashcard_set1, front='palec', back='finger')
        flashcard_factory(owner=user1, flashcard_set=flashcard_set1, front='blady', back='pale')
        flashcard_factory(owner=user1, flashcard_set=flashcard_set2, front='palce', back='fingers')
        flashcard_factory(owner=user2, flashcard_set=flashcard_set3, front='palma', back='palm')
        api_client.force_authenticate(user1)
        url = reverse('flashcard-list')

        response = api_client.get(url + query)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == expected_result


@pytest.mark.django_db
class TestFlashcardList:

    def test_get_flashcards(self, api_client, user_factory, flashcard_set_factory, flashcard_factory):
        user1 = user_factory(username='User1')
        user2 = user_factory(username='User2')
        flashcard_set1 = flashcard_set_factory(owner=user1)
        flashcard_set2 = flashcard_set_factory(owner=user1)
        flashcard_set3 = flashcard_set_factory(owner=user2)
        flashcard_factory.create_batch(size=5, owner=user1, flashcard_set=flashcard_set1)
        flashcard_factory.create_batch(size=2, owner=user1, flashcard_set=flashcard_set2)
        flashcard_factory.create_batch(size=2, owner=user2, flashcard_set=flashcard_set3)
        flashcards = Flashcard.objects.filter(flashcard_set=flashcard_set1)
        serializer = FlashcardSerializer(flashcards, many=True)
        url = reverse('list', kwargs={'flashcard_set_pk': flashcard_set1.pk})
        api_client.force_authenticate(user1)

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 5
        assert response.json()['results'] == serializer.data

    def test_create_flashcard_not_allowed(self, api_client, user, flashcard_set_factory):
        flashcard_set = flashcard_set_factory(owner=user)
        url = reverse('list', kwargs={'flashcard_set_pk': flashcard_set.pk})
        data = {'flashcard_set': flashcard_set.pk, 'front': 'question', 'back': 'answer'}
        api_client.force_authenticate(user)

        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    @pytest.mark.parametrize('query, expected_result', [
        ('?min_date=2021-02-02', 4),
        ('?max_date=2021-02-03', 4),
        ('?min_date=2021-02-02&max_date=2021-02-03', 3)])
    def test_dates(self, query, expected_result, api_client, user_factory, flashcard_set_factory, flashcard_factory):
        user1 = user_factory(username='user1')
        user2 = user_factory(username='user2')
        flashcard_set1 = flashcard_set_factory(owner=user1)
        flashcard_set2 = flashcard_set_factory(owner=user1)
        flashcard_set3 = flashcard_set_factory(owner=user2)
        with freeze_time("2021-01-01"):
            flashcard_factory(owner=user1, flashcard_set=flashcard_set1)
        with freeze_time("2021-02-02"):
            flashcard_factory(owner=user1, flashcard_set=flashcard_set1)
            flashcard_factory(owner=user1, flashcard_set=flashcard_set1)
        with freeze_time("2021-02-03"):
            flashcard_factory(owner=user1, flashcard_set=flashcard_set1)
        flashcard_factory(owner=user1, flashcard_set=flashcard_set1)
        flashcard_factory(owner=user1, flashcard_set=flashcard_set2)
        flashcard_factory(owner=user2, flashcard_set=flashcard_set3)
        url = reverse('list', kwargs={'flashcard_set_pk': flashcard_set1.pk})
        api_client.force_authenticate(user1)

        response = api_client.get(url + query)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == expected_result


@pytest.mark.django_db
@pytest.mark.parametrize('query, expected_result', [
    ('?search=fin', 4),
    ('?search_field=front&search=fin', 2),
    ('?search_field=back&search=fin', 3)])
def test_search_view(query, expected_result, api_client, user, flashcard_set_factory, flashcard_factory):
    flashcard_set = flashcard_set_factory(owner=user)
    flashcard_factory(owner=user, flashcard_set=flashcard_set, front='palec', back='finger')
    flashcard_factory(owner=user, flashcard_set=flashcard_set, front='płetwa', back='fin')
    flashcard_factory(owner=user, flashcard_set=flashcard_set, front='finka', back='sheath knife')
    flashcard_factory(owner=user, flashcard_set=flashcard_set, front='finał', back='final')
    api_client.force_authenticate(user)
    url = reverse('search-set', kwargs={'flashcard_set_pk': flashcard_set.pk})

    response = api_client.get(url + query)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == expected_result
