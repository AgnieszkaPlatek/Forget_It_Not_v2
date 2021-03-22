from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'flashcards', views.FlashcardViewSet, basename='flashcard')
router.register(r'flashcard-sets', views.FlashcardSetViewSet, basename='flashcard-set')


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('flashcard-list/<flashcard_set_pk>/', views.FlashcardListView.as_view(), name='list'),
    path('learn/<flashcard_set_pk>/', views.FlashcardLearnView.as_view(),
         name='learn-list'),
    path('search/<flashcard_set_pk>/', views.SearchView.as_view(),
         name='search-set'),
]
