from django.contrib.auth.models import User
from rest_framework import viewsets

from .models import Flashcard, FlashcardSet
from .serializers import FlashcardSerializer, FlashcardSetSerializer



class FlashcardViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer

    # permission_classes = []

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FlashcardSetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = FlashcardSet.objects.all()
    serializer_class = FlashcardSetSerializer

    # permission_classes = []

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# class SetListView(generics.ListAPIView):
#     serializer_class = SetSerializer
#
#     def get_queryset(self):
#         """
#         This view should return a list of all the sets
#         of the currently authenticated user.
#         """
#         user = User.objects.get(pk=1)  # user = self.request.user
#         return Set.objects.filter(owner=user)
