import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from factories import UserFactory, FlashcardSetFactory, FlashcardFactory


@pytest.fixture
def api_client():
    return APIClient()


register(FlashcardFactory)
register(FlashcardSetFactory)
register(UserFactory)
