from django.urls import path
from .views import FillTransactionView

app_name = 'transactions'


urlpatterns = [
    path('fill/', FillTransactionView.as_view(), name='transaction-fill'),
    # path('withdraw/', WithdrawTransactionView.as_view(), name='transaction-withdraw'),

]
