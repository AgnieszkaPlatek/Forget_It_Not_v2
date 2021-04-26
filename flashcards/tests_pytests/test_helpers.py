import pytest
from django.contrib.auth import get_user_model

from ..helpers import create_example_set
from ..models import Flashcard, FlashcardSet

User = get_user_model()


@pytest.fixture
def user():
    user = User.objects.create(username='Tester', password='Testing321')
    yield user
    user.delete()


@pytest.fixture
def example_set(user):
    create_example_set(user)
    example_set = FlashcardSet.objects.filter(owner=user).last()
    yield example_set
    example_set.delete()


@pytest.mark.django_db
class TestCreateExampleSet:

    def test_example_set_created(self, example_set):
        assert example_set.name == 'example'

    def test_example_set_has_five_flashcards(self, example_set):
        assert Flashcard.objects.filter(flashcard_set=example_set).count() == 5
