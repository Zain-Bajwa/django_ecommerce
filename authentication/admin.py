"""Admin Panel URL Configuration

This file contains all the URLs of the admin panel. This file is used to
connect the URLs to the views. The URLs are used to create, update, delete a
user. It is also used to create new tokens, refresh and verify the tokens. In
this file we have used the rest_framework_simplejwt.views built-in views to
create, refresh and verify the tokens.
"""

from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import User

admin.site.register(User, UserAdmin)

