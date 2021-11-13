from django.db import transaction
from django.db.models import F
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .mixins import CreateModelTransactionMixin
from .models import Transaction
from .serializers import FillTransactionSerializer, WithdrawTransactionSerializer, PayTransactionSerializer
from ..users.models import User
from ..wallets.models import Wallet


# Create your views here.
class FillTransactionView(CreateModelTransactionMixin, GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FillTransactionSerializer

    def perform_create(self, serializer):
        wallet_id = self.request.user.id  # TEMPORARY HARDCODED wallet_id == user_id !! TO BE CHANGED
        wallet = Wallet.objects.get(id=wallet_id)
        wallet.balance = F('balance') + serializer.validated_data.get('value', 0)
        serializer.save(user=self.request.user, type=Transaction.FILL, wallet_id=wallet_id)
        wallet.save(update_fields=['balance'])

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class WithdrawTransactionView(CreateModelTransactionMixin, GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WithdrawTransactionSerializer

    def perform_create(self, serializer):
        wallet_id = self.request.user.id  # TEMPORARY HARDCODED wallet_id == user_id !! TO BE CHANGED
        wallet = Wallet.objects.get(id=wallet_id)
        wallet.balance = F('balance') - serializer.validated_data.get('value', 0)
        serializer.save(user=self.request.user, type=Transaction.WITHDRAW, wallet_id=wallet_id)
        wallet.save(update_fields=['balance'])

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PayTransactionView(CreateModelTransactionMixin, GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PayTransactionSerializer

    def perform_create(self, serializer):

        value = serializer.validated_data.get('value', 0)

        # Sender & Receiver users
        sender = self.request.user
        receiver = User.objects.get(email=serializer.validated_data.pop('email'))

        # Sender wallet
        sender_wallet = Wallet.objects.get(id=sender.id)  # TEMPORARY HARDCODED wallet_id == user_id !! TO BE CHANGED
        sender_wallet.balance = F('balance') - value
        sender_wallet.save(update_fields=['balance'])

        # Receiver wallet
        receiver_wallet = Wallet.objects.get(id=receiver.id)  # TEMPORARY HARDCODED wallet_id == user_id!! TO BE CHANGED
        receiver_wallet.balance = F('balance') + value
        receiver_wallet.save(update_fields=['balance'])

        # Transaction MADE
        serializer.save(user=sender, type=Transaction.MADE, wallet_id=sender_wallet.id, contact=receiver)

        # # Transactions RECEIVED
        Transaction.objects.create(user_id=receiver.id, type=Transaction.RECEIVED, value=value, contact=sender,
                                   wallet=receiver_wallet)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
