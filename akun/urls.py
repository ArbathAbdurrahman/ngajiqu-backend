from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

app_name = 'akun'

urlpatterns = [
    path('', UserProfileAPIView.as_view(), name='user-profile'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', RegistrationView.as_view(), name='register'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]