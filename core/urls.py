"""frontend Application URL Configuration

This file contains all the URLs of the frontend Application. This file is
used to connect the URLs to the views. The URLs are used to create, update,
delete a user. It is also used to create new tokens, refresh and verify the
tokens. In this file we have used the rest_framework_simplejwt.views built-in
views to create, refresh and verify the tokens.
"""


from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import (
    AboutView,
    CartView,
    ContactView,
    HomeView,
    ProductListView,
    ProductDetailView
)

app_name = 'core'
urlpatterns = [
    path("home/",HomeView.as_view(), name="home-view"),
    path('about/', AboutView.as_view(), name='about-view'),
    path('contact/', ContactView.as_view(), name='contact-view'),
    path('products/', ProductListView.as_view(), name='products-view'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product-view'),
    path('cart/', CartView.as_view(), name='cart-view'),
    path('api/', include('core.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)