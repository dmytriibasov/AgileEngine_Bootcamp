import pytest
from django.test import TestCase
from apps.transactions.serializers import (FillTransactionSerializer, WithdrawTransactionSerializer,
                                           PayTransactionSerializer)
from rest_framework.exceptions import ValidationError
from django.test.client import RequestFactory
from rest_framework.test import APIRequestFactory, APIClient

from tests.factories import TransactionFactory, WalletFactory, UserFactory


class TestTransactionSerializer(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.request = APIRequestFactory()
        self.user = UserFactory(email='test_user1@mail.com')
        self.user2 = UserFactory(email='test_user2@mail.com')
        self.client.force_login(user=self.user)
        self.wallet = self.user.wallets.get(id=self.user.id)
        self.data = {
            'value': 100,
            'email': self.user2
        }

    def test_fill_transaction_serializer(self):

        serializer = FillTransactionSerializer(data=self.data)

        assert serializer.is_valid()

    def test_withdraw_transaction_serializer(self):

        self.request.user = self.user
        context = {
            'request': self.request
        }
        serializer = WithdrawTransactionSerializer(data=self.data, context=context)
        serializer.is_valid()

        assert ValidationError
