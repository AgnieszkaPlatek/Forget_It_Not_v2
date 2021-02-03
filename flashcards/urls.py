from django.urls import path, include
from rest_framework_nested import routers

from . import views

# Create a router and register our viewsets with it.
router = routers.SimpleRouter()
router.register(r'flashcard-sets', views.FlashcardSetViewSet)

flashcards_router = routers.NestedSimpleRouter(router, r'flashcard-sets', lookup='flashcard_set')
flashcards_router.register(r'flashcards', views.FlashcardViewSet)


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('', include(flashcards_router.urls)),
    path('search/', views.SearchView.as_view())
]
