from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status

from rest_framework.authtoken.models import Token


User = get_user_model()


class DemoUserGetOrCreate(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = (reverse('demo'))

    def test_new_demo_users_token_created(self):
        response = self.client.put(self.url)
        demo_token = response.data['token']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(demo_token, str(Token.objects.last()))

    def test_new_demo_user_created(self):
        response = self.client.put(self.url)
        demo_token = Token(response.data['token'])
        self.assertEqual(demo_token, User.objects.last().auth_token)

    def test_new_demo_user_has_one_example_set(self):
        response = self.client.put(self.url)
        demo_token = Token(response.data['token'])
        user = User.objects.get(auth_token=demo_token)
        self.assertEqual(user.num_sets, 1)

    def test_new_demo_user_has_five_example_flashcards(self):
        response = self.client.put(self.url)
        demo_token = Token(response.data['token'])
        user = User.objects.get(auth_token=demo_token)
        self.assertEqual(user.num_flashcards, 5)

    def test_demo_user_retrieved_from_cookie(self):
        response = self.client.put(self.url)
        demo_token = Token(response.data['token'])
        response2 = self.client.put(self.url)
        demo_token2 = Token(response2.data['token'])
        self.assertEqual(demo_token, demo_token2)

    def test_two_different_demo_users_when_no_cookie(self):
        response = self.client.put(self.url)
        demo_token = Token(response.data['token'])
        client2 = APIClient()
        response2 = client2.put(self.url)
        demo_token2 = Token(response2.data['token'])
        self.assertNotEqual(demo_token, demo_token2)
