from django.urls import path
from rest_framework import routers

from .views import FillTransactionView, WithdrawTransactionView, PayTransactionView, TransactionsListView

app_name = 'transactions'


# router = routers.SimpleRouter()
#
# router.register('', TransactionModelViewSet, basename='')

urlpatterns = [
    path('fill/', FillTransactionView.as_view(), name='fill'),
    path('withdraw/', WithdrawTransactionView.as_view(), name='withdraw'),
    path('pay/', PayTransactionView.as_view(), name='pay'),
    path('', TransactionsListView.as_view(), name='list'),
]

