from rest_framework import serializers

from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = ('balance', 'currency')
        read_only_fields = fields


class SummarySerializer(serializers.Serializer):

    payments_received = serializers.IntegerField()
    payments_made = serializers.IntegerField()
    withdrawn = serializers.IntegerField()
    filled = serializers.IntegerField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
