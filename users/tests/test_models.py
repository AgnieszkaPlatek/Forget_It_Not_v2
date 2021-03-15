from unittest import skip

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.test import TestCase

from flashcards.models import FlashcardSet, Flashcard
from ..models import User


class UserTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='Tester1', password='Testing321')
        self.set1 = FlashcardSet.objects.create(name='set1', owner=self.user)
        self.set2 = FlashcardSet.objects.create(name='set2', owner=self.user)

    def test_num_sets(self):
        user_sets = FlashcardSet.objects.filter(owner=self.user).count()
        self.assertEqual(user_sets, self.user.num_sets)


    def test_num_flashcards(self):
        Flashcard.objects.create(owner=self.user, flashcard_set=self.set1, front='question1', back='answer1')
        Flashcard.objects.create(owner=self.user, flashcard_set=self.set1, front='question2', back='answer2')
        Flashcard.objects.create(owner=self.user, flashcard_set=self.set1, front='question3', back='answer3')
        Flashcard.objects.create(owner=self.user, flashcard_set=self.set2, front='question4', back='answer4')
        Flashcard.objects.create(owner=self.user, flashcard_set=self.set2, front='question5', back='answer5')
        user_flashcards = Flashcard.objects.filter(owner=self.user).count()
        self.assertEqual(user_flashcards, self.user.num_flashcards)
