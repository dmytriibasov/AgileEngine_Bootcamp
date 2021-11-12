from django.urls import path
from .views import FillTransactionView, WithdrawTransactionView, PayTransactionView

app_name = 'transactions'


urlpatterns = [
    path('fill/', FillTransactionView.as_view(), name='transaction-fill'),
    path('withdraw/', WithdrawTransactionView.as_view(), name='transaction-withdraw'),
    path('pay/', PayTransactionView.as_view(), name='transaction-pay'),
]
