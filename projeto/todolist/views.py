from typing import Tuple
from django.contrib.auth import authenticate

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action

from .permissions import IsAdmin
from .models import Category, TodoList


class AuthView(APIView):

    def get(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

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
        # fields = ['name']


class TodoListSerializer(ModelSerializer):
    # category = SerializerMethodField('_get_categories')
    category = SerializerMethodField(method_name='get_category')

    class Meta:
        model = TodoList
        fields = ['title', 'content', 'date', 'priority', 'category']

    # def _get_categories(self, obj):
    def get_category(self, obj):
        # categories = Category.objects.filter(user=obj.user)
        categories = Category.objects.all()
        # categories = Category.objects.filter(todos=obj)
        serializer = CategorySerializer(categories, many=True)
        return serializer.data


class TodoListViewSet(ModelViewSet):

    serializer_class = TodoListSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return TodoList.objects.filter(user=user).order_by('-priority')


class CategoryViewSet(ModelViewSet):

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Category.objects.filter(user=user).order_by('-name')

    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
