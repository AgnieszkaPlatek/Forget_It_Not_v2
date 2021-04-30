import pytest
from django.db import IntegrityError
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
class TestUser:

    def test_num_sets(self, user, flashcard_set_factory):
        flashcard_set_factory.create_batch(size=5, owner=user)

        assert user.num_sets == 5

    def test_num_flashcards(self, user, flashcard_set_factory, flashcard_factory):
        set1 = flashcard_set_factory(name='set1', owner=user)
        set2 = flashcard_set_factory(name='set2', owner=user)
        flashcard_factory.create_batch(size=5, flashcard_set=set1, owner=user)
        flashcard_factory.create_batch(size=2, flashcard_set=set2, owner=user)

        assert user.num_flashcards == 7

    def test_users_token_created(self, user):
        assert Token.objects.get(user=user) == Token.objects.last()

    def test_fails_to_create_with_existing_username(self, user_factory):
        user_factory(username='Tester')

        with pytest.raises(IntegrityError):
            user_factory(username='Tester')

    def test_not_create_with_existing_email(self, user_factory):
        user_factory(username='Tester', email='email@email.com')

        with pytest.raises(IntegrityError):
            user_factory(username='Tester2', email='email@email.com')
