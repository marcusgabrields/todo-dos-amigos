from typing import Tuple
from django.contrib.auth import authenticate

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authtoken.models import Token

from .permissions import IsAdmin
from .models import Category, TodoList


class AuthView(APIView):

    def get(self, request):
        username = 'admin'
        password = 'admin123'

        user = authenticate(username=username, password=password)

        if user:
            Token.objects.all().delete()
            token = Token.objects.create(user=user)
            return Response({'token': str(token)}, status=200)

        return Response({'fail': True}, status=500)


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class TodoListSerializer(ModelSerializer):

    class Meta:
        model = TodoList
        fields = '__all__'


class TodoListViewSet(ModelViewSet):

    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CategoryViewSet(ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin]
