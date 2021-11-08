from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import NotAuthenticated
from .serializers import SignUpSerializer, LogOutSerializer


class SignUpView(generics.CreateAPIView):
    permission_classes = (NotAuthenticated, )
    queryset = User.objects.all()
    serializer_class = SignUpSerializer


class LogOutView(APIView):
    serializer_class = LogOutSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data={'Logged out'}, status=status.HTTP_204_NO_CONTENT)


class HelloWorldView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        content = {
            'message': 'Hello World'
        }
        return Response(content)
