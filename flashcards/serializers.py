from rest_framework import serializers

from .models import FlashcardSet, Flashcard


class FlashcardSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    owner_name = serializers.CharField(read_only=True)
    set_name = serializers.CharField(read_only=True)
    set_created = serializers.CharField(read_only=True)
    next_id = serializers.IntegerField(read_only=True, allow_null=True)
    previous_id = serializers.IntegerField(read_only=True, allow_null=True)

    class Meta:
        model = Flashcard
        fields = ['id', 'flashcard_set', 'set_name', 'set_created', 'front', 'back', 'owner', 'owner_name', 'added',
                  'last_modified', 'next_id', 'previous_id']


class FlashcardSetSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    flashcards = FlashcardSerializer(many=True, required=False)
    owner_name = serializers.CharField(read_only=True)
    num_flashcards = serializers.CharField(read_only=True)

    class Meta:
        model = FlashcardSet
        fields = ['id', 'name', 'owner', 'owner_name', 'created', 'last_modified', 'num_flashcards', 'flashcards']
