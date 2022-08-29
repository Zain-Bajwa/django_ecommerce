"""User Model

THis is the user model for the authentication app. The user model is used to
communicate with the database. This model is used to create a new user. It is
also used to update and delete a user. This model inherits from the
AbstractUser. This is extend-user model. All the built-in fields are inherited
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """User Model
    This is the user model for the authentication app. The user model is used
    map the user to the database. This model is used to create, update and
    delete a user.
    """

    email = models.EmailField(unique=True, blank=False)
    full_name = models.CharField(max_length=20, blank=True)
    phone_no = models.CharField(max_length=12, blank=True)
    address = models.CharField(max_length=200, blank=True)
    