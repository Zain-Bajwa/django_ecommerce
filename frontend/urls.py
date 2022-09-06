"""frontend Application URL Configuration

This file contains all the URLs of the frontend Application. This file is
used to connect the URLs to the views. The URLs are used to create, update,
delete a user. It is also used to create new tokens, refresh and verify the
tokens. In this file we have used the rest_framework_simplejwt.views built-in
views to create, refresh and verify the tokens.
"""

from django.urls import path
from .views import (
    AboutView,
    ContactView,
    HomeView,
    LoginView,
    ProductView,
    RegisterView,
)

app_name = 'frontend'
urlpatterns = [
    path("home/",HomeView.as_view(), name="home-view"),
    path("login/", LoginView.as_view(), name="login-view"),
    path('register/', RegisterView.as_view(), name='register-view'),
    path('about/', AboutView.as_view(), name='about-view'),
    path('contact/', ContactView.as_view(), name='contact-view'),
    path('products/', ProductView.as_view(), name='products-view'),
]
