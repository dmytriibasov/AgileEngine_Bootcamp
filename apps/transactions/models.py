from datetime import datetime

from django.db import models
from config import settings
from apps.wallets.models import Wallet
from django.db.models import Sum, Q
from django.db.models.functions import Coalesce

class TransactionQuerySet(models.QuerySet):

    def transactions_summary(self):

        return self.aggregate(
            filled=(
                Coalesce(Sum('value', filter=Q(type=Transaction.FILL)), 0)
            ),
            withdrawn=(
                Coalesce(Sum('value', filter=Q(type=Transaction.WITHDRAW)), 0)
            ),
            payments_received=(
                Coalesce(Sum('value', filter=Q(type=Transaction.RECEIVED)), 0)
            ),
            payments_made=(
                Coalesce(Sum('value', filter=Q(type=Transaction.MADE)), 0)
            ),
        )

    def transactions_series(self):
        return self.values('date').annotate(
            filled=(
                Coalesce(Sum('value', filter=Q(type=Transaction.FILL)), 0)
            ),
            withdrawn=(
                Coalesce(Sum('value', filter=Q(type=Transaction.WITHDRAW)), 0)
            ),
            payments_received=(
                Coalesce(Sum('value', filter=Q(type=Transaction.RECEIVED)), 0)
            ),
            payments_made=(
                Coalesce(Sum('value', filter=Q(type=Transaction.MADE)), 0)
            ),
        ).order_by('date')


# Create your models here.
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

    objects = TransactionQuerySet.as_manager()

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
