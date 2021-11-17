import string

import factory
from factory import fuzzy
from config import settings

from apps.transactions.models import Transaction
from apps.wallets.models import Wallet


class UserFactory(factory.django.DjangoModelFactory):

    email = factory.LazyAttribute(lambda a: f'{a.first_name}.{a.last_name}@example.com'.lower())
    first_name = fuzzy.FuzzyText(length=12, chars=string.ascii_letters, prefix='')
    last_name = fuzzy.FuzzyText(length=12, chars=string.ascii_letters, prefix='')

    class Meta:
        model = settings.AUTH_USER_MODEL


class WalletFactory(factory.django.DjangoModelFactory):

    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Wallet


class TransactionFactory(factory.django.DjangoModelFactory):

    user = factory.SubFactory(UserFactory)
    wallet = factory.SubFactory(WalletFactory)
    class Meta:
        model = Transaction
