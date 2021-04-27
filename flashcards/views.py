from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .helpers import CardFrontBackSearchFilter
from .models import Flashcard, FlashcardSet
from .permissions import IsOwner
from .serializers import FlashcardSerializer, FlashcardSetSerializer
from .pagination import PagesCountSmallPagination


class FlashcardViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [CardFrontBackSearchFilter, OrderingFilter]
    ordering_fields = ['front', 'added', 'back']
    pagination_class = None

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class FlashcardSetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = FlashcardSet.objects.all()
    serializer_class = FlashcardSetSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = None

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class FlashcardListView(ListAPIView):
    """View to list, sort and filter flashcards from the set by date."""
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [OrderingFilter]
    ordering_fields = ['front', 'back', 'added']
    pagination_class = PagesCountSmallPagination

    def get_queryset(self):
        self.queryset = self.queryset.filter(owner=self.request.user, flashcard_set=self.kwargs.get('flashcard_set_pk'))
        min_date = self.request.GET.get('min_date')
        max_date = self.request.GET.get('max_date')
        if min_date:
            self.queryset = self.queryset.filter(added__gte=min_date)
        if max_date:
            self.queryset = self.queryset.filter(added__lte=max_date)
        return self.queryset


class FlashcardLearnView(FlashcardListView):
    """Non-paginated view to filter flashcards by date for learning part of the set,
    to enable passing more flashcards to learning session and for browsing flashcards"""
    filter_backends = []
    ordering_fields = []
    pagination_class = None


class SearchView(ListAPIView):
    """View to search for a flashcard in the set."""
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [CardFrontBackSearchFilter]
    pagination_class = None

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user, flashcard_set=self.kwargs.get('flashcard_set_pk'))
