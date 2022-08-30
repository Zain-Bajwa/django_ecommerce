"""Authentication Application URL Configuration

This file contains all the URLs of the authentication Application. This file is
used to connect the URLs to the views. The URLs are used to create, update,
delete a user. It is also used to create new tokens, refresh and verify the
tokens. In this file we have used the rest_framework_simplejwt.views built-in
views to create, refresh and verify the tokens.
"""

from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenRefreshView, TokenVerifyView)
from .views import UserRegisterView, UserViewSet, AllUserViewSet, CreateTokenView

router = routers.DefaultRouter()

# For retrieve, update, and delete a user
router.register('user', UserViewSet, basename='user-view')
# For retrieve all the users
router.register('users', AllUserViewSet, basename='user-view')

urlpatterns = [
    path('register/user/', UserRegisterView.as_view(), name='register-user'),
    path('token/create/', CreateTokenView.as_view(), name='create-token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('token/verify/', TokenVerifyView.as_view(), name='verify-token'),
]

urlpatterns += router.urls
