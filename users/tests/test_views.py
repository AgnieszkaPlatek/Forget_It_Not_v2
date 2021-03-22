from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status

from rest_framework.authtoken.models import Token


User = get_user_model()


class DemoUserCreate(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = (reverse('demo-create'))

    def test_new_demo_user_created(self):
        response = self.client.post(self.url)
        user = User.objects.get(username=response.data['username'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user, User.objects.last())

    def test_new_demo_users_token_created(self):
        response = self.client.post(self.url)
        user = User.objects.get(username=response.data['username'])
        self.assertEqual(Token.objects.get(user=user), Token.objects.last())

    def test_new_demo_user_has_one_example_set(self):
        response = self.client.post(self.url)
        user = User.objects.get(username=response.data['username'])
        self.client.force_authenticate(user=user)
        self.assertEqual(user.num_sets, 1)

    def test_demo_user_has_five_example_flashcards(self):
        response = self.client.post(self.url)
        user = User.objects.get(username=response.data['username'])
        self.client.force_authenticate(user=user)
        self.assertEqual(user.num_flashcards, 5)
