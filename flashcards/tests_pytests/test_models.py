import pytest
from django.contrib.auth import get_user_model

from ..models import FlashcardSet, Flashcard

User = get_user_model()


@pytest.fixture
def user1():
    user1 = User.objects.create(username='Tester1', password='Testing321')
    yield user1
    user1.delete()


@pytest.fixture
def user2():
    user2 = User.objects.create(username='Tester2', password='Testing321')
    yield user2
    user2.delete()


@pytest.fixture
def set1(user1):
    set1 = FlashcardSet.objects.create(name="set1", owner=user1)
    yield set1
    set1.delete()


@pytest.fixture
def set2(user2):
    set2 = FlashcardSet.objects.create(name="set2", owner=user2)
    yield set2
    set2.delete()


@pytest.mark.django_db
class TestFlashcardSet:
    def test_owner_name(self, set1):
        assert set1.owner_name == 'Tester1'

    def test_num_flashcards(self, user1, user2, set1, set2):
        Flashcard.objects.create(owner=user1, flashcard_set=set1, front='question1', back='answer1')
        Flashcard.objects.create(owner=user1, flashcard_set=set1, front='question2', back='answer2')
        Flashcard.objects.create(owner=user2, flashcard_set=set2, front='question3', back='answer3')
        assert set1.num_flashcards == 2

    def test_str(self, set1):
        assert str(set1) == 'set1'


@pytest.fixture
def flashcard1(user1, set1):
    flashcard1 = Flashcard.objects.create(owner=user1, flashcard_set=set1, front='question1', back='answer1')
    yield flashcard1
    flashcard1.delete()


@pytest.mark.django_db
class TestFlashcard:

    def test_get_all_user_flashcards(self, user1, user2, set1, set2):
        set3 = FlashcardSet.objects.create(name='set3', owner=user2)
        Flashcard.objects.create(owner=user1, flashcard_set=set1, front='question1', back='answer1')
        Flashcard.objects.create(owner=user1, flashcard_set=set1, front='question2', back='answer2')
        Flashcard.objects.create(owner=user1, flashcard_set=set2, front='question3', back='answer3')
        Flashcard.objects.create(owner=user1, flashcard_set=set2, front='question4', back='answer4')
        Flashcard.objects.create(owner=user2, flashcard_set=set3, front='question5', back='answer5')
        assert Flashcard.objects.filter(owner=user1).count() == 4

    def test_get_all_flashcards_from_one_flashcard_set(self, user1, set1):
        set2 = FlashcardSet.objects.create(name='set2', owner=user1)
        Flashcard.objects.create(owner=user1, flashcard_set=set1, front='question1', back='answer1')
        Flashcard.objects.create(owner=user1, flashcard_set=set1, front='question2', back='answer2')
        Flashcard.objects.create(owner=user1, flashcard_set=set2, front='question3', back='answer3')
        assert Flashcard.objects.filter(flashcard_set=set1).count() == 2

    def test_owner_name(self, flashcard1):
        assert flashcard1.owner_name == 'Tester1'

    def test_set_name(self, flashcard1):
        assert flashcard1.set_name == 'set1'

    def test_set_created(self, set1, flashcard1):
        date_created = set1.created
        assert flashcard1.set_created == date_created

    def test_str(self, flashcard1):
        assert str(flashcard1) == 'question1 - answer1'
