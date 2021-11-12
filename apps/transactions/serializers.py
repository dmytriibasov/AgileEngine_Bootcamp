from rest_framework import serializers
from .models import Transaction


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
        field = ['value']
