import pytest

from ..helpers import create_example_set
from ..models import Flashcard, FlashcardSet


@pytest.fixture
def example_set(user):
    create_example_set(user)
    example_set = FlashcardSet.objects.filter(owner=user).last()
    yield example_set
    example_set.delete()


@pytest.mark.django_db
class TestCreateExampleSet:

    def test_example_set_created1(self, example_set):
        assert example_set.name == 'example'

    def test_example_set_has_five_flashcards1(self, example_set):
        assert Flashcard.objects.filter(flashcard_set=example_set).count() == 5
