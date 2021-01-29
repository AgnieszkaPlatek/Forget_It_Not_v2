from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Flashcard, FlashcardSet
from .permissions import IsOwner
from .serializers import FlashcardSerializer, FlashcardSetSerializer


class FlashcardViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(owner=self.request.user)


class FlashcardSetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = FlashcardSet.objects.all()
    serializer_class = FlashcardSetSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(owner=self.request.user)
