from django.db import models

<<<<<<< HEAD
# Create your models here.
=======
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
>>>>>>> 2e415a1 (Set code format)
