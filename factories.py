import factory
from faker import Faker

from flashcards.models import FlashcardSet, Flashcard
from users.models import User

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = fake.unique.first_name_nonbinary()


class FlashcardSetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FlashcardSet

    owner = factory.SubFactory(UserFactory)
    name = fake.word()


class FlashcardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Flashcard

    owner = factory.SubFactory(UserFactory)
    flashcard_set = factory.SubFactory(FlashcardSetFactory)
    front = fake.word()
    back = fake.word()
