import secrets

from rest_framework import status
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from flashcards.helpers import create_example_set
from .models import User
from .serializers import UserSerializer, DemoTokenUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API url that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # permission_classes = []


class DemoTokenView(APIView):
    """
    API url for getting or creating demo users.
    Returns demo user token to enable token authenticatoin with demo user's account.
    """
    def put(self, request):
        if 'demo' in request.COOKIES:
            demo_username = request.COOKIES['demo']
            demo_user = User.objects.get(username=demo_username)
            demo_token = Token.objects.get(user=demo_user)
            serializer = DemoTokenUserSerializer(data={'token': str(demo_token)})
            return Response(serializer.initial_data, status=status.HTTP_200_OK)

        else:
            demo_username = secrets.token_urlsafe(16)
            demo_user = User.objects.create(username=demo_username, password='Testing321')
            create_example_set(demo_user)
            demo_token = Token.objects.get(user=demo_user)
            serializer = DemoTokenUserSerializer(data={'token': str(demo_token)})
            response = Response(serializer.initial_data, status=status.HTTP_201_CREATED)
            response.set_cookie(key='demo', value=demo_username)
            return response
