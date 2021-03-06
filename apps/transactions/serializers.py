from rest_framework import serializers
from .models import Transaction
from ..users.models import User


class FillTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['value']

    def validate_value(self, value):
        if value <= 0:
            raise serializers.ValidationError("Value must be greater than 0.")
        return value


class WithdrawTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['value']

    def validate_value(self, value):
        if value <= 0:
            raise serializers.ValidationError("Value must be greater than 0.")
        return value

    def validate(self, attrs):
        user = self.context.get('request').user
        wallet = user.wallets.get(id=user.id)
        balance = wallet.balance

        if attrs['value'] > balance:
            raise serializers.ValidationError('Transaction is not possible. Insufficient balance.')
        return attrs


class PayTransactionSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()

    class Meta:
        model = Transaction
        fields = ['value', 'email']

    def validate_value(self, value):
        if value <= 0:
            raise serializers.ValidationError("Value must be greater than 0.")
        return value

    def validate_email(self, value):

        request = self.context.get('request')
        current_user = request.user

        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email doesn't exist")
        elif User.objects.get(email=value) == current_user:
            raise serializers.ValidationError("It's not allowed to use own email")
        return value

    def validate(self, attrs):
        user = self.context['request'].user
        wallet = user.wallets.get(id=user.id)
        balance = wallet.balance

        if attrs['value'] > balance:
            raise serializers.ValidationError('Transaction is not possible. Insufficient balance.')
        return attrs


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['date', 'value', 'type']
        read_only_fields = fields
