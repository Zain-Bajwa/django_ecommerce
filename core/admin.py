"""Admin Panel URL Configuration for Core App

This file contains all the URLs of the admin panel. This file is used to
connect the URLs to the views.
"""

from django.contrib import admin
from core.models import Product, Category, Order, Cart


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Cart)
