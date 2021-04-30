import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def demo_token(api_client):
    response = api_client.put(reverse('demo'))
    demo_token = Token(response.data['token'])
    yield demo_token
    demo_token.delete()


@pytest.mark.django_db
class TestDemoUser:

    def test_new_demo_users_token_created(self, api_client):
        response = api_client.put(reverse('demo'))
        demo_token = Token(response.data['token'])

        assert response.status_code == status.HTTP_201_CREATED
        assert demo_token == Token.objects.last()

    def test_new_demo_user_created(self, demo_token):
        assert demo_token == User.objects.last().auth_token

    def test_new_demo_user_has_one_example_set(self, demo_token):
        user = User.objects.get(auth_token=demo_token)

        assert user.num_sets == 1

    def test_new_demo_user_has_five_example_flashcards(self, demo_token):
        user = User.objects.get(auth_token=demo_token)

        assert user.num_flashcards == 5

    def test_demo_user_retrieved_from_cookie(self, api_client, demo_token):
        response2 = api_client.put(reverse('demo'))
        demo_token2 = Token(response2.data['token'])

        assert demo_token == demo_token2

    def test_two_different_demo_users_when_no_cookie(self, demo_token):
        api_client2 = APIClient()
        response2 = api_client2.put(reverse('demo'))
        demo_token2 = Token(response2.data['token'])

        assert demo_token != demo_token2
