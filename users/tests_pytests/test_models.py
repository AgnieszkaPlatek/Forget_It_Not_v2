import pytest
from django.db import IntegrityError
from rest_framework.authtoken.models import Token

from flashcards.models import FlashcardSet, Flashcard
from ..models import User


@pytest.fixture
def user1():
    user1 = User.objects.create(username='Tester1', password='Testing321')
    yield user1
    user1.delete()


@pytest.fixture
def set1(user1):
    set1 = FlashcardSet.objects.create(name="set1", owner=user1)
    yield set1
    set1.delete()


@pytest.fixture
def set2(user1):
    set2 = FlashcardSet.objects.create(name="set2", owner=user1)
    yield set2
    set2.delete()


@pytest.mark.django_db
class TestUser:

    def test_num_sets(self, user1, set1, set2):
        assert user1.num_sets == 2

    def test_num_flashcards(self, user1, set1, set2):
        Flashcard.objects.create(owner=user1, flashcard_set=set1, front='question1', back='answer1')
        Flashcard.objects.create(owner=user1, flashcard_set=set1, front='question2', back='answer2')
        Flashcard.objects.create(owner=user1, flashcard_set=set1, front='question3', back='answer3')
        Flashcard.objects.create(owner=user1, flashcard_set=set2, front='question4', back='answer4')
        Flashcard.objects.create(owner=user1, flashcard_set=set2, front='question5', back='answer5')
        assert user1.num_flashcards == 5

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
