import datetime
from django.db.models import F
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import Transaction
from .serializers import FillTransactionSerializer, WithdrawTransactionSerializer, PayTransactionSerializer,\
    TransactionSerializer
from ..users.models import User
from ..wallets.models import Wallet


# Create your views here.
class FillTransactionView(CreateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = FillTransactionSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            wallet_id = self.request.user.id  # TEMPORARY HARDCODED wallet_id == user_id !! TO BE CHANGED
            wallet = Wallet.objects.get(id=wallet_id)
            wallet.balance = F('balance') + serializer.validated_data.get('value', 0)
            serializer.save(user=self.request.user, type=Transaction.FILL, wallet_id=wallet_id)
            wallet.save(update_fields=['balance'])


class WithdrawTransactionView(CreateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = WithdrawTransactionSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            wallet_id = self.request.user.id  # TEMPORARY HARDCODED wallet_id == user_id !! TO BE CHANGED
            wallet = Wallet.objects.get(id=wallet_id)
            wallet.balance = F('balance') - serializer.validated_data.get('value', 0)
            serializer.save(user=self.request.user, type=Transaction.WITHDRAW, wallet_id=wallet_id)
            wallet.save(update_fields=['balance'])


class PayTransactionView(CreateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = PayTransactionSerializer

    def perform_create(self, serializer):

        value = serializer.validated_data.get('value', 0)

        # Sender & Receiver users
        sender = self.request.user
        receiver = User.objects.get(email=serializer.validated_data.get('email'))

        # Wallets for Sender & Receiver
        sender_wallet = Wallet.objects.get(id=sender.id)  # TEMPORARY HARDCODED wallet_id == user_id !! TO BE CHANGED
        receiver_wallet = Wallet.objects.get(id=receiver.id)  # TEMPORARY HARDCODED wallet_id == user_id!! TO BE CHANGED

        with transaction.atomic():

            # Update sender wallet balance
            sender_wallet.balance = F('balance') - value
            sender_wallet.save(update_fields=['balance'])

            # Update receiver wallet balance
            receiver_wallet.balance = F('balance') + value
            receiver_wallet.save(update_fields=['balance'])

            # Transaction MADE
            serializer.save(user=sender, type=Transaction.MADE, wallet_id=sender_wallet.id, email=receiver)

            # # Transactions RECEIVED
            Transaction.objects.create(user_id=receiver.id, type=Transaction.RECEIVED, value=value, email=sender,
                                       wallet=receiver_wallet)


class TransactionsListView(ListAPIView):

    permission_classes = (IsAuthenticated,)
    pagination_class = LimitOffsetPagination
    serializer_class = TransactionSerializer

    def get_queryset(self):
        queryset = self.request.user.transactions.all()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date', datetime.datetime.today())
        if start_date and end_date:
            queryset = queryset.filter(date__range=(start_date, end_date))
        elif end_date:
            queryset = queryset.filter(date__lte=end_date)
        return queryset.order_by('id')
