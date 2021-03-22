from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User


class FlashcardSet(models.Model):
    """
    Set model is a set of flashcards.
    User can create as many sets as he likes.
    """
    name = models.CharField(max_length=20, verbose_name=_('name'))
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created']

    @property
    def owner_name(self):
        return self.owner.username

    @property
    def num_flashcards(self):
        return Flashcard.objects.filter(flashcard_set=self).count()

    def __str__(self):
        return self.name


class Flashcard(models.Model):
    """
    Flashcard model, each flashcard belongs to one set.
    """
    flashcard_set = models.ForeignKey(FlashcardSet, related_name='flashcards', on_delete=models.CASCADE)
    front = models.CharField(max_length=50, verbose_name=_('front'))
    back = models.CharField(max_length=50, verbose_name=_('back'))
    added = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['added']

    @property
    def owner_name(self):
        return self.owner.username

    @property
    def set_name(self):
        return self.flashcard_set.name

    @property
    def set_created(self):
        return self.flashcard_set.created

    def __str__(self):
        return f'{self.front} - {self.back}'
