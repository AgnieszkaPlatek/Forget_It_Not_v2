from rest_framework import serializers

from .models import FlashcardSet, Flashcard


class FlashcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flashcard
        fields = ['id', 'flashcard_set', 'front', 'back', 'owner', 'added', 'last_modified']


class FlashcardSetSerializer(serializers.ModelSerializer):
    flashcards = FlashcardSerializer(many=True, read_only=True)

    class Meta:
        model = FlashcardSet
        fields = ['id', 'name', 'owner', 'created', 'last_modified', 'flashcards']
