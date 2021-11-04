from django.urls import path
from .views import SignUpView, UsersList

app_name = 'users'


urlpatterns = [
    path('', UsersList.as_view()),
    path('signup/', SignUpView.as_view()),
]

