import pytest
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from apps.users.models import User
from apps.transactions.models import Transaction
from tests.factories import TransactionFactory, WalletFactory, UserFactory


class TestTransactionApiView(TestCase):

    def setUp(self) -> None:

        self.client = APIClient()

    # @pytest.mark.django_db
    def test_transaction_fill(self):
        user = UserFactory()
        self.client.force_login(user=user)

        data = {
            'value': 100,
        }

        response = self.client.post(reverse('transactions:fill'), data=data)

        assert response.status_code == 201

    # def test_transaction_withdraw(self):
    #     user2 = UserFactory()
    #     wallet2 = WalletFactory(user=user2, balance=200)
    #     self.client.force_login(user=user2)
    #
    #     print(f'BALANCE: {wallet2.balance} ID: {wallet2.id}')
    #     data = {
    #         'value': 100,
    #     }
    #
    #     response = self.client.post(reverse('transactions:withdraw'), data=data)
    #
    #     assert response.status_code == 201
