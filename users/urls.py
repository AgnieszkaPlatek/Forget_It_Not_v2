from django.urls import path

from . import views


urlpatterns = [
    path('demo/', views.DemoTokenView.as_view(),
         name='demo'),
]
