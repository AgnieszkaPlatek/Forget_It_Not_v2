from rest_framework import viewsets
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
import secrets
from rest_framework import status
from rest_framework.views import APIView
from flashcards.helpers import create_example_set


class UserViewSet(viewsets.ModelViewSet):
    """
    API url that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # permission_classes = []


class DemoUserCreateView(APIView):
    """
    API url for creating demo users.
    """
    def post(self, request):
        demo_username = secrets.token_urlsafe(16)
        serializer = UserSerializer(data={"username": demo_username, "password": "Testing321"})
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=demo_username)
            create_example_set(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
