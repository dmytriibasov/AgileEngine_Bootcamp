import pytest

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from apps.users.models import User
from apps.transactions.models import Transaction
from tests.factories import TransactionFactory, WalletFactory, UserFactory


class TestTransactionApi:
    client = APIClient()

    @pytest.mark.django_db
    def test_transaction_fill(self):
        user = UserFactory()
        wallet = WalletFactory(user=user)
        self.client.force_login(user=user)

        data = {
            'value': 100,
        }

        response = self.client.post(reverse('transactions:fill'), data=data)

        assert response.status_code == 201
        # wallet.refresh_from_db()
        # assert wallet.balance == data['value']   ????

    # @pytest.mark.django_db
    # def test_transaction_withdraw(self):
    #     user = UserFactory()
    #     wallet = WalletFactory(user=user, balance=200)
    #     self.client.force_login(user=user)
    #     print(f'BALANCE: {wallet.balance}')
    #     data = {
    #         'value': 100,
    #         # 'user': user,
    #         # 'type': Transaction.WITHDRAW,
    #         # 'wallet': wallet
    #     }
    #
    #     response = self.client.post(reverse('transactions:withdraw'), data=data)
    #
    #     assert response.status_code == 201
