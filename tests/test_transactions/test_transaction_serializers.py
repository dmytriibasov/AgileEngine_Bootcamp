import pytest
from apps.transactions.serializers import (FillTransactionSerializer, WithdrawTransactionSerializer,
                                           PayTransactionSerializer)
from rest_framework.exceptions import ValidationError


@pytest.mark.django_db
def test_fill_transaction_serializer():
    data = {
        'value': 100,
    }

    serializer = FillTransactionSerializer(data=data)
    assert serializer.is_valid()


@pytest.mark.django_db
def test_withdraw_transaction_serializer():
    data = {
        'value': 100,
    }
    serializer = WithdrawTransactionSerializer(data=data)
    assert serializer.is_valid()

    data = {
        'value': 0,
    }
    serializer = WithdrawTransactionSerializer(data=data)
    assert not serializer.is_valid()
    # assert ValidationError


@pytest.mark.django_db
def test_pay_transaction_serializer():
    data = {
        'value': 100,
        'email': 'testuser@mail.com'
    }
    serializer = PayTransactionSerializer(data=data)
    assert serializer.is_valid()

    data = {
        'value': 0,
        'email': 'testuser@mail.com'
    }
    serializer = PayTransactionSerializer(data=data)
    assert ValidationError
    assert not serializer.is_valid()
