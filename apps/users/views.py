from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import SignUpSerializer, LogOutSerializer


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer


class LogOutView(APIView):

    serializer_class = LogOutSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
        # try:
        #     refresh_token = request.data['refresh']
        #     token = RefreshToken(refresh_token)
        #     token.blacklist()
        # except Exception as e:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)


class HelloWorldView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        content = {
            'message': 'Hello World'
        }
        return Response(content)
