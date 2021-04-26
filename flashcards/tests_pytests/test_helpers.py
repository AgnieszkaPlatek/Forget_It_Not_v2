import pytest
from django.contrib.auth import get_user_model

from ..helpers import create_example_set
from ..models import Flashcard, FlashcardSet

User = get_user_model()


@pytest.fixture
def example_set(user1):
    create_example_set(user1)
    example_set = FlashcardSet.objects.filter(owner=user1).last()
    yield example_set
    example_set.delete()


@pytest.mark.django_db
class TestCreateExampleSet:

    def test_example_set_created(self, example_set):
        assert example_set.name == 'example'

    def test_example_set_has_five_flashcards(self, example_set):
        assert Flashcard.objects.filter(flashcard_set=example_set).count() == 5
