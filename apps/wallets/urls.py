from django.urls import path
from rest_framework import routers

from .views import WalletView, SummaryView, SeriesView

app_name = 'wallet'


urlpatterns = [
    path('information/balance/', WalletView.as_view(), name='balance'),
    path('information/summary/', SummaryView.as_view(), name='summary'),
    path('information/series/', SeriesView.as_view(), name='series'),
]
