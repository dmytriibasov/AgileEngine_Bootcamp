from django.db import transaction
from django.db.models import F
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Transaction
from .serializers import FillTransactionSerializer, WithdrawTransactionSerializer


# Create your views here.
from ..wallets.models import Wallet


class FillTransactionView(CreateAPIView):

    permission_classes = (IsAuthenticated, )
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
        serializer.save(user=self.request.user, type=Transaction.FILL, wallet_id=wallet_id)
        Wallet.objects.filter(id=wallet_id).update(balance=F('balance') + serializer.validated_data.get('value', 0))


# class WithdrawTransactionView(CreateAPIView):
#     permission_classes = (IsAuthenticated, )
#     serializer_class = WithdrawTransactionSerializer
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             with transaction.atomic():
#                 self.perform_create(serializer)
#                 headers = self.get_success_headers(serializer.data)
#                 return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#
#     def perform_create(self, serializer):
#         wallet_id = self.request.user.id  # TEMPORARY HARDCODED wallet_id == user_id !! TO BE CHANGED
#         serializer.save(user=self.request.user, type=Transaction.WITHDRAW, wallet_id=wallet_id)
#         Wallet.objects.filter(id=wallet_id).update(balance=F('balance') - serializer.validated_data.get('value', 0))
