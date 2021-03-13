from unittest import skip

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.test import TestCase

from flashcards.models import FlashcardSet, Flashcard
from users.models import User


class FlashcardSetTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='Tester1', password='Testing321')

    def test_create_flashcard_set(self):
        set1 = FlashcardSet.objects.create(name="set1", owner=self.user)
        self.assertIn(set1, FlashcardSet.objects.filter(owner=self.user))

    def test_get_all_user_flashcard_sets(self):
        FlashcardSet.objects.create(name='set1', owner=self.user)
        FlashcardSet.objects.create(name='set2', owner=self.user)
        self.assertEqual(2, FlashcardSet.objects.filter(owner=self.user).count())

    def test_rename_flashcard_set(self):
        set_pk = FlashcardSet.objects.create(name='set1', owner=self.user).pk
        flashcard_set = FlashcardSet.objects.get(pk=set_pk)
        flashcard_set.name = 'my_set'
        flashcard_set.save()
        self.assertEqual('my_set', FlashcardSet.objects.get(pk=set_pk).name)

    def test_delete_flashcard_set(self):
        flashcard_set = FlashcardSet.objects.create(name='flashcard_set', owner=self.user)
        pk = flashcard_set.pk
        flashcard_set.delete()
        with self.assertRaises(ObjectDoesNotExist):
            FlashcardSet.objects.get(pk=pk)

    def test_owner_name(self):
        set1 = FlashcardSet.objects.create(name="set1", owner=self.user)
        self.assertEqual(set1.owner_name, self.user.username)

    def test_num_flashcards(self):
        set1 = FlashcardSet.objects.create(name="set1", owner=self.user)
        Flashcard.objects.create(owner=self.user, flashcard_set=set1, front='question1', back='answer1')
        Flashcard.objects.create(owner=self.user, flashcard_set=set1, front='question2', back='answer2')
        self.assertEqual(2, set1.num_flashcards)


class FlashcardTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='Tester1', password='Testing321')
        self.set1 = FlashcardSet.objects.create(name='set1', owner=self.user1)

    def test_create_flashcard_with_all_fields_given(self):
        flashcard = Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question', back='answer')
        self.assertIn(flashcard, Flashcard.objects.filter(owner=self.user1))

    def test_raise_integrity_error_while_creating_with_missing_flashcard_set(self):
        with self.assertRaises(IntegrityError):
            Flashcard.objects.create(owner=self.user1, front='question', back='answer')

    @skip
    def test_raise_integrity_error_while_creating_with_missing_front(self):
        with self.assertRaises(IntegrityError):
            Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, back='answer1')
            # Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question2')

    @skip
    def test_raise_integrity_error_while_creating_with_missing_back(self):
        with self.assertRaises(IntegrityError):
            Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question2')

    def test_update_flashcard(self):
        flashcard_pk = Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question',
                                                back='answer').pk
        flashcard = Flashcard.objects.get(pk=flashcard_pk)
        flashcard.front = 'new_question'
        flashcard.save()
        self.assertEqual('new_question', Flashcard.objects.get(pk=flashcard_pk).front)

    def test_delete_flashcard(self):
        flashcard = Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question', back='answer')
        pk = flashcard.pk
        flashcard.delete()
        with self.assertRaises(ObjectDoesNotExist):
            Flashcard.objects.get(pk=pk)

    # def test_fail_to_update_with_flashcard_set_given_but_no_front_and_no_back(self):
    #     pass

    def test_to_get_all_users_flashcards(self):
        self.user2 = User.objects.create(username='Tester2', password='Testing321')
        self.set2 = FlashcardSet.objects.create(name='set2', owner=self.user1)
        self.set3 = FlashcardSet.objects.create(name='set3', owner=self.user2)
        Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question1', back='answer1')
        Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question2', back='answer2')
        Flashcard.objects.create(owner=self.user1, flashcard_set=self.set2, front='question3', back='answer3')
        Flashcard.objects.create(owner=self.user1, flashcard_set=self.set2, front='question4', back='answer4')
        Flashcard.objects.create(owner=self.user2, flashcard_set=self.set3, front='question5', back='answer5')
        self.assertEqual(4, Flashcard.objects.filter(owner=self.user1).count())

    def test_to_get_all_flashcards_from_one_flashcard_set(self):
        self.set2 = FlashcardSet.objects.create(name='set2', owner=self.user1)
        Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question1', back='answer1')
        Flashcard.objects.create(owner=self.user1, flashcard_set=self.set1, front='question2', back='answer2')
        Flashcard.objects.create(owner=self.user1, flashcard_set=self.set2, front='question3', back='answer3')
        self.assertEqual(2, Flashcard.objects.filter(flashcard_set=self.set1).count())
