import pytest
from django.contrib.auth import get_user_model
from pytest_factoryboy import register
from rest_framework.test import APIClient

from factories import UserFactory, FlashcardSetFactory, FlashcardFactory
from flashcards.models import FlashcardSet

User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user1():
    user1 = User.objects.create(username='Tester1', password='Testing321')
    yield user1
    user1.delete()


@pytest.fixture
def user2():
    user2 = User.objects.create(username='Tester2', password='Testing321')
    yield user2
    user2.delete()


@pytest.fixture
def set1(user1):
    set1 = FlashcardSet.objects.create(name="set1", owner=user1)
    yield set1
    set1.delete()


@pytest.fixture
def set2(user1):
    set2 = FlashcardSet.objects.create(name="set2", owner=user1)
    yield set2
    set2.delete()


@pytest.fixture
def set3(user2):
    set3 = FlashcardSet.objects.create(name="set3", owner=user2)
    yield set3
    set3.delete()


register(FlashcardFactory)
register(FlashcardSetFactory)
register(UserFactory)
