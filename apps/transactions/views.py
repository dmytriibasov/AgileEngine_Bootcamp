from django.db import transaction
from django.db.models import F
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Transaction
from .serializers import FillTransactionSerializer, WithdrawTransactionSerializer, PayTransactionSerializer

# Create your views here.
from ..users.models import User
from ..wallets.models import Wallet


class FillTransactionView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FillTransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        wallet_id = self.request.user.id  # TEMPORARY HARDCODED wallet_id == user_id !! TO BE CHANGED
        wallet = Wallet.objects.get(id=wallet_id)
        wallet.balance = F('balance') + serializer.validated_data.get('value', 0)
        serializer.save(user=self.request.user, type=Transaction.FILL, wallet_id=wallet_id)
        wallet.save(update_fields=['balance'])


class WithdrawTransactionView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WithdrawTransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        wallet_id = self.request.user.id  # TEMPORARY HARDCODED wallet_id == user_id !! TO BE CHANGED
        wallet = Wallet.objects.get(id=wallet_id)
        wallet.balance = F('balance') - serializer.validated_data.get('value', 0)
        serializer.save(user=self.request.user, type=Transaction.WITHDRAW, wallet_id=wallet_id)
        wallet.save(update_fields=['balance'])


class PayTransactionView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PayTransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):

        value = serializer.validated_data.get('value', 0)
        print(f'VALUE: {value}')
        # Sender & Receiver users
        sender = self.request.user
        print(f'SENDER: {sender}')
        receiver = User.objects.get(email=serializer.validated_data.get('email'))
        print(f'RECEIVER {receiver}')
        # Sender wallet
        sender_wallet = Wallet.objects.get(id=sender.id)  # TEMPORARY HARDCODED wallet_id == user_id !! TO BE CHANGED
        sender_wallet.balance = F('balance') - value
        print(f'SENDER BALANCE: {sender_wallet.balance}')
        sender_wallet.save(update_fields=['balance'])

        # Receiver wallet
        receiver_wallet = Wallet.objects.get(id=receiver.id)  # TEMPORARY HARDCODED wallet_id == user_id!! TO BE CHANGED
        receiver_wallet.balance = F('balance') + value
        print(f'RECEIVER BALANCE: {receiver_wallet.balance}')
        receiver_wallet.save(update_fields=['balance'])

        # Transaction MADE
        serializer.save(user=sender, type=Transaction.MADE, wallet_id=sender_wallet.id, contact=receiver)

        # Transactions RECEIVED
        Transaction.objects.create(user=receiver, value=value, type=Transaction.RECEIVED,
                                   wallet_id=receiver_wallet.id, contact=sender)
