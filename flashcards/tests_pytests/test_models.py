import pytest
from django.contrib.auth import get_user_model

from ..models import Flashcard

User = get_user_model()


@pytest.fixture
def flashcard1(user1, set1):
    flashcard1 = Flashcard.objects.create(owner=user1, flashcard_set=set1, front='question1', back='answer1')
    yield flashcard1
    flashcard1.delete()


@pytest.mark.django_db
class TestFlashcardSet:
    def test_owner_name(self, set1):
        assert set1.owner_name == 'Tester1'

    def test_num_flashcards(self, user1, set1, set2, flashcard_factory):
        flashcard_factory.create_batch(size=3, owner=user1, flashcard_set=set1)
        flashcard_factory.create_batch(size=2, owner=user1, flashcard_set=set2)
        assert set1.num_flashcards == 3

    def test_str(self, set1):
        assert str(set1) == 'set1'


@pytest.mark.django_db
class TestFlashcard:

    def test_get_all_user_flashcards(self, user1, user2, set1, set2, set3, flashcard_factory):
        flashcard_factory.create_batch(size=3, owner=user1, flashcard_set=set1)
        flashcard_factory.create_batch(size=2, owner=user1, flashcard_set=set2)
        flashcard_factory.create_batch(size=2, owner=user2, flashcard_set=set3)
        assert Flashcard.objects.filter(owner=user1).count() == 5

    def test_get_all_flashcards_from_one_flashcard_set(self, user1, set1, set2, flashcard_factory):
        flashcard_factory.create_batch(size=3, owner=user1, flashcard_set=set1)
        flashcard_factory.create_batch(size=2, owner=user1, flashcard_set=set2)
        assert Flashcard.objects.filter(flashcard_set=set1).count() == 3

    def test_owner_name(self, flashcard1):
        assert flashcard1.owner_name == 'Tester1'

    def test_set_name(self, flashcard1):
        assert flashcard1.set_name == 'set1'

    def test_set_created(self, set1, flashcard1):
        date_created = set1.created
        assert flashcard1.set_created == date_created

    def test_str(self, flashcard1):
        assert str(flashcard1) == 'question1 - answer1'
