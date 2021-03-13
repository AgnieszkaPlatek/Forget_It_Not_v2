from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from django.test import TestCase
from unittest import skip
from rest_framework.test import APIClient

from flashcards.models import FlashcardSet, Flashcard
from users.models import User


# class FlashcardSetTest(TestCase):
#
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.user = User.objects.create(username="tester")
#         client = APIClient()
#         client.force_authenticate(user=self.user)
#
#     def test_create_flashcard_set(self):
#         response = self.client.post('api/flashcard-sets/', {'name': 'testing'})
#         self.assertEqual(response.status_code, 201)
#         # self.assertEqual('testing', FlashcardSet.objects.get(owner=self.user))
#
#     @skip
#     def test_get_all_users_flashcard_sets(self):
#         pass
#
#     @skip
#     def test_rename_flashcard_set(self):
#         pass
#
#     @skip
#     def test_delete_flashcard_set(self):
#         pass

# class FlashcardTest(TestCase):
#
#     def setUp(self):
#         pass
#
#     def test_create_flashcard_with_all_fields_given(self):
#         pass
#
#     def test_fail_to_create_if_missing_flashcard_set(self):
#         pass
#
#     def test_fail_to_create_if_missing_front_or_back(self):
#         pass
#
#     def test_update_flashcard_with_flashcard_set_and_one_field_given(self):
#         pass
#
#     def test_fail_to_update_with_no_flashcard_set_given(self):
#         pass
#
#     def test_fail_to_update_with_flashcard_set_given_but_no_front_and_no_back(self):
#         pass

# def test_to_get_all_users_flashcards(self):
#     pass
#
# def test_to_get_all_flashcards_from_one_flashcard_set(self):
#     pass
#
# def test_delete_flashcard(self):
#     pass
