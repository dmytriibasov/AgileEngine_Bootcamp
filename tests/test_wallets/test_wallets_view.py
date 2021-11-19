import pytest
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from apps.users.models import User
from apps.transactions.models import Transaction
from tests.factories import TransactionFactory, WalletFactory, UserFactory
from django.db.models import F


class TestBalanceApiView(TestCase):

    def setUp(self) -> None:

        self.client = APIClient()
        self.user = User.objects.create(email='test_TESTuser@mail.com')
        self.wallet = self.user.wallets.get(id=self.user.id)
        self.client.force_login(user=self.user)
        self.user2 = User.objects.create(email='test_TESTuser_2@mail.com')

    def test_balance_api_view(self):

        self.wallet.balance = 1000
        self.wallet.save(update_fields=['balance'])

        response = self.client.get(reverse('wallets:balance'))

        assert response.status_code == 200
        assert response.data == {'balance': 1000}

    def test_summary_api_view(self):

        response = self.client.get(reverse('wallets:summary'))

        data = {
            'payments_received': 0,
            'payments_made': 0,
            'filled': 0,
            'withdrawn': 0
        }

        assert response.status_code == 200
        assert response.data == data

    def test_series_api_view(self):

        Transaction.objects.create(user=self.user, type=Transaction.FILL, value=500, date='2021-11-17',
                                   wallet=self.wallet)
        Transaction.objects.create(user=self.user, type=Transaction.WITHDRAW, value=100, date='2021-11-18',
                                   wallet=self.wallet)
        Transaction.objects.create(user=self.user, type=Transaction.MADE, value=100, date='2021-11-19',
                                   email=self.user2, wallet=self.wallet)
        Transaction.objects.create(user=self.user, type=Transaction.RECEIVED, value=200, date='2021-11-19',
                                   email=self.user2, wallet=self.wallet)

        response = self.client.get(reverse('wallets:series'))

        print(f'{response.data}')
        assert response.status_code == 200
        assert response.data == {}
