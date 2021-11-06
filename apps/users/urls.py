from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import SignUpView, HelloWorldView, LogOutView

app_name = 'users'


urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('hello/', HelloWorldView.as_view(), name='hello'),
]

