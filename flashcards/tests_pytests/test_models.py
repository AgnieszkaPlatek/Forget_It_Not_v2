import pytest

from ..models import Flashcard


@pytest.mark.django_db
class TestFlashcardSet:
    def test_owner_name(self, user_factory, flashcard_set_factory):
        user = user_factory(username='Tester')
        flashcard_set = flashcard_set_factory(owner=user)

        assert flashcard_set.owner_name == 'Tester'

    def test_num_flashcards(self, user, flashcard_set_factory, flashcard_factory):
        flashcard_set1 = flashcard_set_factory(owner=user)
        flashcard_set2 = flashcard_set_factory(owner=user)
        flashcard_factory.create_batch(size=3, owner=user, flashcard_set=flashcard_set1)
        flashcard_factory.create_batch(size=2, owner=user, flashcard_set=flashcard_set2)

        assert flashcard_set1.num_flashcards == 3

    def test_str(self, flashcard_set_factory):
        flashcard_set = flashcard_set_factory(name='test_set')

        assert str(flashcard_set) == 'test_set'


@pytest.mark.django_db
class TestFlashcard:

    def test_get_all_user_flashcards(self, user_factory, flashcard_set_factory, flashcard_factory):
        user1 = user_factory(username='user1')
        user2 = user_factory(username='user2')
        flashcard_set1 = flashcard_set_factory(owner=user1)
        flashcard_set2 = flashcard_set_factory(owner=user1)
        flashcard_set3 = flashcard_set_factory(owner=user2)
        flashcard_factory.create_batch(size=3, owner=user1, flashcard_set=flashcard_set1)
        flashcard_factory.create_batch(size=2, owner=user1, flashcard_set=flashcard_set2)
        flashcard_factory.create_batch(size=2, owner=user2, flashcard_set=flashcard_set3)

        assert Flashcard.objects.filter(owner=user1).count() == 5

    def test_get_all_flashcards_from_one_flashcard_set(self, user, flashcard_set_factory, flashcard_factory):
        flashcard_set1 = flashcard_set_factory(owner=user)
        flashcard_set2 = flashcard_set_factory(owner=user)
        flashcard_factory.create_batch(size=3, owner=user, flashcard_set=flashcard_set1)
        flashcard_factory.create_batch(size=2, owner=user, flashcard_set=flashcard_set2)

        assert Flashcard.objects.filter(flashcard_set=flashcard_set1).count() == 3

    def test_owner_name(self, user_factory, flashcard_factory):
        user = user_factory(username='Tester')
        flashcard = flashcard_factory(owner=user)

        assert flashcard.owner_name == 'Tester'

    def test_set_name(self, user, flashcard_set_factory, flashcard_factory):
        flashcard_set = flashcard_set_factory(name='test_set', owner=user)
        flashcard = flashcard_factory(flashcard_set=flashcard_set, owner=user)

        assert flashcard.set_name == 'test_set'

    def test_set_created(self, user, flashcard_set_factory, flashcard_factory):
        flashcard_set = flashcard_set_factory(owner=user)
        flashcard = flashcard_factory(flashcard_set=flashcard_set, owner=user)
        date_created = flashcard_set.created

        assert flashcard.set_created == date_created

    def test_str(self, user_factory, flashcard_factory):
        user = user_factory(username='Tester')
        flashcard = flashcard_factory(front='question', back='answer', owner=user)

        assert str(flashcard) == 'question - answer'
