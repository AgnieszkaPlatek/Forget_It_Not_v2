from django.contrib.auth import get_user_model
from django.test import TestCase

from ..helpers import create_example_set
from ..models import FlashcardSet, Flashcard

User = get_user_model()


class CreateExampleSetTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='Tester', password='Testing321')
        create_example_set(self.user)
        self.example_set = FlashcardSet.objects.filter(owner=self.user).last()

    def test_example_set_created(self):
        self.assertEqual(self.example_set.name, 'example')

    def test_example_set_has_five_flashcards(self):
        num_flashcards = Flashcard.objects.filter(flashcard_set=self.example_set).count()
        self.assertEqual(num_flashcards, 5)
