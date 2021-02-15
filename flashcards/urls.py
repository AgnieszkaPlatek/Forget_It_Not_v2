from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

# router = routers.SimpleRouter()
# router.register(r'flashcard-sets', views.FlashcardSetViewSet)
#
# flashcards_router = routers.NestedSimpleRouter(router, r'flashcard-sets', lookup='flashcard_set')
# flashcards_router.register(r'flashcards', views.FlashcardViewSet)
#
#
# # The API URLs are now determined automatically by the router.
# urlpatterns = [
#     path('', include(router.urls)),
#     path('', include(flashcards_router.urls)),
#     path('search/', views.SearchView.as_view())
# ]

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'flashcards', views.FlashcardViewSet)
router.register(r'flashcard-sets', views.FlashcardSetViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('flashcard-list/<flashcard_set_pk>/', views.FlashcardListView.as_view()),
]