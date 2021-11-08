from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.http import request
from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    """
    Serializer for signing up.
    """
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'first_name', 'last_name', 'birth_date']
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}}
        }

    def save(self):
        user = User(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            birth_date=self.validated_data['birth_date'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user


class LogOutSerializer(serializers.Serializer):
    """
    Serializer to blacklist refresh token while logging out.
    """
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': 'Token is expired or invalid'
    }

    def validate(self, attrs):
        self.token = attrs.get('refresh')

        return attrs

    def save(self, **kwargs):

        try:
            refresh_token = RefreshToken(self.token)
            refresh_token.blacklist()

        except TokenError:
            self.fail('bad_token')
