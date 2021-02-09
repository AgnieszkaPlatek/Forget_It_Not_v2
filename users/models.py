from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token


class User(AbstractUser):

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Token.objects.get_or_create(user=self)
