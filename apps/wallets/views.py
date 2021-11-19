import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Wallet
from .serializers import WalletSerializer, SummarySerializer, SeriesSerializer
from .services import CurrencyConverter


# Create your views here.
class WalletView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        wallet = Wallet.objects.get(id=self.request.user.id)
        currency_converter = CurrencyConverter(currency=self.request.query_params.get('currency', wallet.currency),
                                               base_currency=wallet.currency)

        data = {
            'balance': currency_converter.converted_amount(wallet.balance)
        }
        serializer = WalletSerializer(instance=data)
        return Response(data=serializer.data)


class SummaryView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):

        wallet = Wallet.objects.get(id=self.request.user.id)
        currency_converter = CurrencyConverter(currency=self.request.query_params.get('currency', wallet.currency),
                                               base_currency=wallet.currency)

        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date', datetime.datetime.today())

        if start_date and end_date:
            queryset = request.user.transactions.filter(date__range=(start_date, end_date)).transactions_summary()
        else:
            queryset = request.user.transactions.filter(date__lte=end_date).transactions_summary()

        data = {key: currency_converter.converted_amount(value) for key, value in queryset.items()}

        serializer = SummarySerializer(instance=data)
        return Response(data=serializer.data)


class SeriesView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date', datetime.datetime.today())

        if start_date and end_date:
            queryset = request.user.transactions.filter(date__range=(start_date, end_date)).transactions_series()
        else:
            queryset = request.user.transactions.filter(date__lte=end_date).transactions_series()

        wallet = Wallet.objects.get(id=self.request.user.id)
        currency_converter = CurrencyConverter(currency=self.request.query_params.get('currency', wallet.currency),
                                               base_currency=wallet.currency)
        data = {}

        for query in queryset:
            for key in query:
                data[key] = []

        for query in queryset:
            for key, value in query.items():
                if key == 'date':
                    data[key].append(value)
                data[key].append(currency_converter.converted_amount(value))

        serializer = SeriesSerializer(instance=data)
        return Response(data=serializer.data)
