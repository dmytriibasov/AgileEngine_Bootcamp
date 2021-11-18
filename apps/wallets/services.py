import requests
from django.conf import settings
from django.core.cache import cache
from openexchangerate import OpenExchangeRates


class CurrencyConverter:

    currencies = {'USD': None, 'EUR': None, 'UAH': None}
    base_currency = 'USD'

    client = OpenExchangeRates(api_key=settings.CURRENCY_EXCHANGE_APP_ID, local_base=base_currency)

    def __init__(self, currency='USD', base_currency='USD'):
        self.base_currency = base_currency.upper()
        self.currency = currency.upper()
        self._is_valid()

    def converted_amount(self, amount):
        amount *= self.exchange_ratio
        return amount

    @property
    def exchange_ratio(self):

        exchange_currency_rate = cache.get(self.currency)
        if not exchange_currency_rate:
            exchange_currency_rate = self.client.latest().dict.get(self.currency)
            cache.set(self.currency, exchange_currency_rate, 300)

        return exchange_currency_rate

    def _is_valid(self):
        if (self.base_currency and self.currency) in self.currencies:
            return True
        else:
            raise Exception("Entered currencies are not available")
