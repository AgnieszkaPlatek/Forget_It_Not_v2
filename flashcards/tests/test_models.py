from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import FlashcardSet, Flashcard

User = get_user_model()


class FlashcardSetTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='Tester1', password='Testing321')
        self.user2 = User.objects.create(username='Tester2', password='Testing321')

    def test_owner_name(self):
        set1 = FlashcardSet.objects.create(name="set1", owner=self.user1)
        self.assertEqual(set1.owner_name, 'Tester1')

    def test_num_flashcards(self):
        set1 = FlashcardSet.objects.create(name="example", owner=self.user1)
        set2 = FlashcardSet.objects.create(name="example", owner=self.user2)
        Flashcard.objects.create(owner=self.user1, flashcard_set=set1, front='question1', back='answer1')
        Flashcard.objects.create(owner=self.user1, flashcard_set=set1, front='question2', back='answer2')
        Flashcard.objects.create(owner=self.user2, flashcard_set=set2, front='question3', back='answer3')
        self.assertEqual(set1.num_flashcards, 2)

    def test_str(self):
        flashcard_set = FlashcardSet.objects.create(owner=self.user1, name='my-set')
        self.assertEqual(str(flashcard_set), 'my-set')


class FlashcardTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='Tester1', password='Testing321')
        self.set1 = FlashcardSet.objects.create(name='set1', owner=self.user1)

    def test_to_get_all_user_flashcards(self):
        self.user2 = User.objects.create(username='Tester2', password='Testing321')
        self.set2 = FlashcardSet.objects.create(name='set2', owner=self.user1)
        self.set3 = FlashcardSet.objects.create(name='set3', owner=self.user2)
        Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question1', back='answer1')
        Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question2', back='answer2')
        Flashcard.objects.create(owner=self.user1, flashcard_set=self.set2, front='question3', back='answer3')
        Flashcard.objects.create(owner=self.user1, flashcard_set=self.set2, front='question4', back='answer4')
        Flashcard.objects.create(owner=self.user2, flashcard_set=self.set3, front='question5', back='answer5')
        self.assertEqual(Flashcard.objects.filter(owner=self.user1).count(), 4)

    def test_to_get_all_flashcards_from_one_flashcard_set(self):
        self.set2 = FlashcardSet.objects.create(name='set2', owner=self.user1)
        Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question1', back='answer1')
        Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question2', back='answer2')
        Flashcard.objects.create(owner=self.user1, flashcard_set=self.set2, front='question3', back='answer3')
        self.assertEqual(Flashcard.objects.filter(flashcard_set=self.set1).count(), 2)

    def test_owner_name(self):
        flashcard = Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question1',
                                             back='answer1')
        self.assertEqual(flashcard.owner_name, 'Tester1')

    def test_set_name(self):
        flashcard = Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question1',
                                             back='answer1')
        self.assertEqual(flashcard.set_name, 'set1')

    def test_set_created(self):
        date_created = self.set1.created
        flashcard = Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question1',
                                             back='answer1')
        self.assertEqual(flashcard.set_created, date_created)

    def test_str(self):
        flashcard = Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question', back='answer')
        self.assertEqual(str(flashcard), 'question - answer')
