from rest_framework import serializers
from .models import User


class MyUserSerializer(serializers.ModelSerializer):
    num_flashcards = serializers.CharField(read_only=True)
    num_sets = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'num_sets', 'num_flashcards']


class DemoTokenUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['token']
