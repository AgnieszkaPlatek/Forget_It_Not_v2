from rest_framework import filters
from flashcards.models import FlashcardSet, Flashcard


class CardFrontBackSearchFilter(filters.SearchFilter):
    """
    Enables the user to specify search fields and if none are chosen both fields are used.
    """
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_field', ['front', 'back'])


def create_example_set(guest_user):
    example_set = FlashcardSet.objects.create(name='example', owner=guest_user)
    examples = [('kot', 'cat'), ('pies', 'dog'), ('koń', 'horse'), ('krowa', 'cow'), ('mysz', 'mouse')]
    for example in examples:
        Flashcard.objects.create(flashcard_set=example_set, owner=guest_user, front=example[0], back=example[1])
