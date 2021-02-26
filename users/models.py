from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Token.objects.get_or_create(user=self)

    @property
    def num_sets(self):
        from flashcards.models import FlashcardSet
        return FlashcardSet.objects.filter(owner=self).count()

    @property
    def num_flashcards(self):
        from flashcards.models import Flashcard
        return Flashcard.objects.filter(owner=self).count()
