from django.db import models
from config import settings


# Create your models here.
from apps.wallets.models import Wallet


class Transaction(models.Model):

    FILL = 'FILL'
    WITHDRAW = 'WITHDRAW'
    RECEIVED = 'RECEIVED'
    MADE = 'MADE'
    TRANSACTION_TYPES = [
        (FILL, 'payment_fill'),
        (WITHDRAW, 'payment_withdraw'),
        (RECEIVED, 'payment_received'),
        (MADE, 'payment_made'),
    ]

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions',
    )

    type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES,
    )

    value = models.PositiveIntegerField()

    date = models.DateField(
        auto_now_add=True,
    )

    contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )

    wallet = models.ForeignKey(
        to=Wallet,
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
