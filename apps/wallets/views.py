import datetime

from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Wallet
from .serializers import WalletSerializer, SummarySerializer, SeriesSerializer
from .services import CurrencyConverter


# Create your views here.
# class WalletView(RetrieveAPIView):
#
#     permission_classes = (IsAuthenticated,)
#     serializer_class = WalletSerializer
#     queryset = Wallet.objects.all()
#
#     def get_object(self):
#         queryset = self.filter_queryset(self.get_queryset())
#         obj = queryset.get(pk=self.request.user.id)
#         self.check_object_permissions(self.request, obj)
#
#         return obj

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

        data = {key: (value if not value else currency_converter.converted_amount(value))
                for key, value in queryset.items()}

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
            print(f'{queryset}')


        data = {}
        for query in queryset:
            for key in query:
                data[key] = []

        wallet = Wallet.objects.get(id=self.request.user.id)
        currency_converter = CurrencyConverter(currency=self.request.query_params.get('currency', wallet.currency),
                                               base_currency=wallet.currency)

        for query in queryset:
            for key, value in query.items():
                if key == 'date' or not value:
                    data[key].append(value)
                else:
                    data[key].append(currency_converter.converted_amount(value))

        serializer = SeriesSerializer(instance=data)
        return Response(data=serializer.data)
