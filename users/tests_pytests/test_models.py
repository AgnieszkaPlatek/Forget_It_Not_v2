import pytest
from django.db import IntegrityError
from rest_framework.authtoken.models import Token

from ..models import User


@pytest.mark.django_db
class TestUser:

    def test_num_sets(self, user1, set1, set2):
        assert user1.num_sets == 2

    def test_num_flashcards(self, flashcard_factory, user1, set1, set2):
        flashcard_factory.create_batch(size=5, flashcard_set=set1, owner=user1)
        flashcard_factory.create_batch(size=2, flashcard_set=set2, owner=user1)
        assert user1.num_flashcards == 7

    def test_users_token_created(self, user1):
        assert Token.objects.get(user=user1) == Token.objects.last()

    def test_fails_to_create_with_existing_username(self):
        User.objects.create(username='Tester', password='Testing543')
        with pytest.raises(IntegrityError):
            User.objects.create(username='Tester', password='Testing543')

    def test_not_create_with_existing_email(self):
        User.objects.create(username='User1', password='Testing321', email='email@email.com')
        with pytest.raises(IntegrityError):
            User.objects.create(username='User2', password='Testing543', email='email@email.com')
