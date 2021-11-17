from django.db.models import F, Func, Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Wallet
from ..transactions.models import Transaction
from ..users.models import User


@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(id=instance.id, user=instance)  # TEMPORARY HARDCODED wallet_id == user_id!! TO CHANGE
