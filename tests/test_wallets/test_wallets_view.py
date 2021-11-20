import pytest
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from apps.transactions.models import Transaction
from datetime import datetime
from tests.factories import UserFactory


class TestBalanceApiView(TestCase):

    def setUp(self, *summary_data) -> None:

        self.client = APIClient()
        self.user = UserFactory(email='test_user1@mail.com')
        self.wallet = self.user.wallets.get(id=self.user.id)
        self.client.force_login(user=self.user)
        self.user2 = UserFactory(email='test_user2@mail.com')
        self.data = summary_data

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

        assert response.data == data
        assert response.status_code == 200

    def test_series_api_view(self):

        Transaction.objects.create(user=self.user, type=Transaction.FILL, value=555, wallet=self.wallet)
        Transaction.objects.create(user=self.user, type=Transaction.WITHDRAW, value=333, wallet=self.wallet)
        Transaction.objects.create(user=self.user, type=Transaction.MADE, value=111, email=self.user2,
                                   wallet=self.wallet)
        Transaction.objects.create(user=self.user, type=Transaction.RECEIVED, value=222, email=self.user2,
                                   wallet=self.wallet)

        t = Transaction.objects.get(user=self.user, type=Transaction.RECEIVED)
        t.date = datetime(2021, 11, 17)
        t.save(update_fields=['date'])

        response = self.client.get(reverse('wallets:series'))

        transactions_series_data = {
            'payments_made': [0, 111],
            'payments_received': [222, 0],
            'filled': [0, 555],
            'withdrawn': [0, 333],
            'dates': ['2021-11-17', datetime.now().date().isoformat()]
        }

        assert response.status_code == 200
        assert response.data == transactions_series_data
