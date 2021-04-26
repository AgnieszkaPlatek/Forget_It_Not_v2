import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def demo_url():
    return reverse('demo')


@pytest.mark.django_db
class TestDemoUser:

    def test_new_demo_users_token_created(self, client, demo_url):
        response = client.put(demo_url)
        demo_token = response.data['token']
        assert response.status_code == status.HTTP_201_CREATED
        assert demo_token == str(Token.objects.last())

    def test_new_demo_user_created(self, client, demo_url):
        response = client.put(demo_url)
        demo_token = Token(response.data['token'])
        assert demo_token == User.objects.last().auth_token

    def test_new_demo_user_has_one_example_set(self, client, demo_url):
        response = client.put(demo_url)
        demo_token = Token(response.data['token'])
        user = User.objects.get(auth_token=demo_token)
        assert user.num_sets == 1

    def test_new_demo_user_has_five_example_flashcards(self, client, demo_url):
        response = client.put(demo_url)
        demo_token = Token(response.data['token'])
        user = User.objects.get(auth_token=demo_token)
        assert user.num_flashcards == 5

    def test_demo_user_retrieved_from_cookie(self, client, demo_url):
        response = client.put(demo_url)
        demo_token = Token(response.data['token'])
        response2 = client.put(demo_url)
        demo_token2 = Token(response2.data['token'])
        assert demo_token == demo_token2

    def test_two_different_demo_users_when_no_cookie(self, client, demo_url):
        response = client.put(demo_url)
        demo_token = Token(response.data['token'])
        client2 = APIClient()
        response2 = client2.put(demo_url)
        demo_token2 = Token(response2.data['token'])
        assert demo_token != demo_token2
