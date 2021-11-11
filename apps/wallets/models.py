from django.db import models
from config import settings


# Create your models here.
class Wallet(models.Model):

    USD = 'USD'
    EUR = 'EUR'
    UAH = 'UAH'

    CURRENCIES = [
        (USD, 'USD'),
        (EUR, 'EUR'),
        (UAH, 'UAH'),
    ]

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wallets'
    )

    balance = models.PositiveIntegerField(
        default=0,
    )

    currency = models.CharField(
        max_length=5,
        choices=CURRENCIES,
        default=USD,
    )

    class Meta:
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'

