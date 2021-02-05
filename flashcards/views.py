from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .helpers import CustomSearchFilter
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
    filter_backends = [CustomSearchFilter]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        self.queryset = self.queryset.filter(owner=self.request.user, flashcard_set=self.kwargs['flashcard_set_pk'])
        min_date = self.request.GET.get('min_date')
        max_date = self.request.GET.get('max_date')
        if min_date:
            self.queryset = self.queryset.filter(added__gte=min_date)
        if max_date:
            self.queryset = self.queryset.filter(added__lte=max_date)
        return self.queryset


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
        return self.queryset.filter(owner=self.request.user)


class SearchView(ListAPIView):
    """
    View to search for flashcards in all user's flashcards from different sets.
    """
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [CustomSearchFilter]

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
