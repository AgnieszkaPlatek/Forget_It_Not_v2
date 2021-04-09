from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    email = models.EmailField(unique=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Token.objects.get_or_create(user=self)

    @property
    def num_sets(self):
        return self.flashcardset_set.count()

    @property
    def num_flashcards(self):
        return self.flashcard_set.count()
