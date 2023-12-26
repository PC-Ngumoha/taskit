""" Contains route definitions for this specific app """
from authentication.views import (
    UserRegisterView, UserLoginView, AuthUserView)
from django.urls import path

urlpatterns = [
    path('register', UserRegisterView.as_view(), name='user-register'),
    path('login', UserLoginView.as_view(), name='user-login'),
    path('me', AuthUserView.as_view(), name='authenticated-user'),
]
