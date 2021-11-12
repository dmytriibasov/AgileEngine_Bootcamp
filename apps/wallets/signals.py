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


# @receiver(post_save, sender=Transaction)
# def update_balance(sender, instance, created, **kwargs):
#     if created:
#         transaction = instance
#         user = transaction.user
#         wallet = transaction.wallet
#         if transaction.FILL:
#             balance = Transaction.objects.filter(user=user).aggregate((Sum('value')))
#             print(balance['value__sum'])
#             Wallet.objects.filter(id=user.id).update(balance=balance['value__sum'])
