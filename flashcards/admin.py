from django.contrib import admin

from .models import Flashcard, FlashcardSet


@admin.register(FlashcardSet)
class FlashcardSetAdmin(admin.ModelAdmin):
    model = FlashcardSet
    list_display = ('id', 'name', 'owner', 'created')
    list_filter = ('owner', 'created')
    search_fields = ('name', 'owner')


@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    model = Flashcard
    list_display = ('id', '__str__', 'owner', 'flashcard_set', 'added')
    list_filter = ('flashcard_set', 'owner', 'added')
    search_fields = ('front', 'back', 'flashcard_set', 'owner')