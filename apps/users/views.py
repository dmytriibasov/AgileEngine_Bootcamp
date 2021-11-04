from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from .models import User
from .serializers import SignUpSerializer


class UsersList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer




