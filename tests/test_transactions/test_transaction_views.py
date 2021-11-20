import pytest
from django.test import TestCase
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from apps.users.models import User
from apps.transactions.models import Transaction
from tests.factories import TransactionFactory, WalletFactory, UserFactory


class TestTransactionApiView(TestCase):

    def setUp(self) -> None:

        self.client = APIClient()
        self.user = UserFactory(email='test_user1@mail.com')
        self.user2 = UserFactory(email='test_user2@mail.com')
        self.client.force_login(user=self.user)
        self.wallet = self.user.wallets.get(id=self.user.id)

    # Test FILL Transaction endpoint
    def test_transaction_fill(self):

        data = {'value': 100}

        response = self.client.post(reverse('transactions:fill'), data=data)

        assert response.status_code == 201  # check response status code
        assert Transaction.objects.all().count() == 1    # check whether transaction is saved in db

        transaction = Transaction.objects.latest('id')

        assert transaction.wallet.balance == data.get('value')   # check if wallet balance was updated

    # Test WITHDRAW Transaction endpoint
    def test_transaction_withdraw(self):

        self.wallet.balance = 300
        self.wallet.save(update_fields=['balance'])

        data_1 = {'value': 100}

        response = self.client.post(reverse('transactions:withdraw'), data=data_1)

        assert response.status_code == 201   # check response status code
        assert Transaction.objects.all().count() == 1    # check whether transaction is saved in db

        data_2 = {'value': 300}

        response = self.client.post(reverse('transactions:withdraw'), data=data_2)
        transaction = Transaction.objects.latest('id')

        assert transaction.wallet.balance < data_2.get('value')  # check when wallet balance less then transaction value

        data_3 = {'value': 'some string'}

        response = self.client.post(reverse('transactions:withdraw'), data=data_3)

        assert ValidationError   # check when entered value - not int object

    # Test PAY Transaction endpoint
    def test_transaction_pay(self):

        self.wallet.balance = 1000
        self.wallet.save(update_fields=['balance'])

        test_data = {'value': 200, 'email': 'test_user2@mail.com'}

        response = self.client.post(reverse('transactions:pay'), data=test_data)

        assert response.status_code == 201   # check response status code
        assert Transaction.objects.all().count() == 2  # Transactions PAY and MADE should be created.

        transaction_made = Transaction.objects.filter(user=self.user).latest('id')
        transaction_received = Transaction.objects.filter(user=self.user2).latest('id')

        assert transaction_made.wallet.balance == self.wallet.balance - test_data.get('value')
        assert transaction_received.wallet.balance == test_data.get('value')

