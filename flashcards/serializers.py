from rest_framework import serializers

from .models import FlashcardSet, Flashcard


class FlashcardSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlashcardSet
        fields = ['name', 'owner', 'created', 'last_modified']


class FlashcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flashcard
        fields = ['flashcard_set', 'front', 'back', 'owner', 'added', 'last_modified']
