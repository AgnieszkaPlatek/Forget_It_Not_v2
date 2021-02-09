from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .helpers import CardFrontBackSearchFilter
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
    filter_backends = [CardFrontBackSearchFilter, OrderingFilter]
    ordering_fields = ['front', 'added']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        # Version of get_queryset when not using rest_framework_nested
        return self.queryset.filter(owner=self.request.user)

        # Version of get_queryset when using rest_framework_nested
        # self.queryset = self.queryset.filter(owner=self.request.user, flashcard_set=self.kwargs['flashcard_set_pk'])
        # min_date = self.request.GET.get('min_date')
        # max_date = self.request.GET.get('max_date')
        # if min_date:
        #     self.queryset = self.queryset.filter(added__gte=min_date)
        # if max_date:
        #     self.queryset = self.queryset.filter(added__lte=max_date)
        # return self.queryset


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

    # My alternative solution with filtering by date but no searching and ordering when not using rest_framework_nested
    @action(detail=True)
    def flashcards(self, request, pk=None):
        flashcards = Flashcard.objects.filter(flashcard_set=pk)
        min_date = self.request.GET.get('min_date')
        max_date = self.request.GET.get('max_date')
        if min_date:
            flashcards = flashcards.filter(added__gte=min_date)
        if max_date:
            flashcards = flashcards.filter(added__lte=max_date)
        serializer = FlashcardSerializer(flashcards, many=True)
        return Response(serializer.data)


class FlashcardListView(ListAPIView):
    # I wanted nested flashcards to have this functionality.
    """
    View to filter, sort and search for flashcards in a set.
    """
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [CardFrontBackSearchFilter, OrderingFilter]
    ordering_fields = ['front', 'added']

    def get_queryset(self):
        self.queryset = self.queryset.filter(owner=self.request.user, flashcard_set=self.kwargs.get('flashcard_set_pk'))
        min_date = self.request.GET.get('min_date')
        max_date = self.request.GET.get('max_date')
        if min_date:
            self.queryset = self.queryset.filter(added__gte=min_date)
        if max_date:
            self.queryset = self.queryset.filter(added__lte=max_date)
        return self.queryset


class SearchView(ListAPIView):
    # This is needed when using rest_framework_nested.
    """
    View to search for flashcards in all user's flashcards from different sets.
    """
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [CardFrontBackSearchFilter]

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
