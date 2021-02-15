from rest_framework import serializers

from .models import FlashcardSet, Flashcard


class FlashcardSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(read_only=True)
    set_name = serializers.CharField(read_only=True)
    set_created = serializers.CharField(read_only=True)

    class Meta:
        model = Flashcard
        fields = ['id', 'flashcard_set', 'set_name', 'set_created', 'front', 'back', 'owner', 'owner_name', 'added',
                  'last_modified']


class FlashcardSetSerializer(serializers.ModelSerializer):
    flashcards = FlashcardSerializer(many=True)
    owner_name = serializers.CharField(read_only=True)

    class Meta:
        model = FlashcardSet
        fields = ['id', 'name', 'owner', 'owner_name', 'created', 'last_modified', 'flashcards']
