<<<<<<< HEAD
"""User Model

THis is the user model for the authentication app. The user model is used to
communicate with the database. This model is used to create a new user. It is
also used to update and delete a user. This model inherits from the
AbstractUser. This is extend-user model. All the built-in fields are inherited
"""

=======
"""User and Product Model

This is the model for User and product. The user model is used to communicate
with the database. This model is used to create a new user. It is also used to
update and delete a user. This model inherits from the AbstractUser. This is
extend-user model. All the built-in fields are inherited.The Product model is
used to create a new product. It is also used to update and delete a product.
This model inherits from the models.Model. This file is also includes the model
for the Order and Cart
"""

import datetime
>>>>>>> f2553bb (Add product api in authentication app)
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """User Model
    This is the user model for the authentication app. The user model is used
<<<<<<< HEAD
    map the user to the database. This model is used to create, update and
    delete a user.
    """

    email = models.EmailField(
        unique=True, blank=False, default=None, null=True
    )
    full_name = models.CharField(max_length=20, blank=True)
    phone_no = models.CharField(max_length=12, blank=True)
    address = models.CharField(max_length=200, blank=True)
=======
    to map the user to the database. This model is used to create, update and
    delete a user. In this model we extend user with followimg fields:
    - email
    - full name
    - address
    - phone number
    """

    email = models.EmailField(
        unique=True, blank=False, default=None, null=True
    )
    full_name = models.CharField(max_length=20, blank=True)
    phone_no = models.CharField(max_length=12, blank=True)
    address = models.CharField(max_length=200, blank=True)


class Category(models.Model):
    """Category Model
    This is the category model for the authentication app. The category model
    is used to map the category to the database. This model is used to create,
    update and delete a category.
    """

    name = models.CharField(max_length=50, unique=True, blank=False)

    # pylint: disable=too-few-public-methods
    class Meta:
        """Meta class"""
        ordering = ["name"]


class Product(models.Model):
    """Product Model

    This is the product model for the authentication app. The product model is
    used to map the product to the database. This model is used to create,
    update and delete a product. In this model we used the foreign key to map
    the category to the product.
    In this model we used the fields stock and sold to keep track of the stock.

    """

    name = models.CharField(max_length=60, unique=True, blank=False)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(
        Category, on_delete=models.RESTRICT, blank=False
    )
    stock = models.IntegerField(default=0)
    sold = models.IntegerField(default=0)
    description = models.CharField(
        max_length=250, default="", blank=True, null=True
    )


class Order(models.Model):
    """Order Model

    The Order model is used to map the order to the database. This model is
    used to create, update and delete a order. In this model we used the
    foreign key to map the user to the order.
    """

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    price = models.IntegerField(default=0)
    address = models.CharField(max_length=50, default="", blank=True)
    phone = models.CharField(max_length=50, default="", blank=True)
    date_created = models.DateField(default=datetime.datetime.today)


class OrderItem(models.Model):
    """OrderItem Model

    The OrderItem model is used to map the order item to the database. This
    model is used to create, update and delete a order item. In this model we
    used the foreign key to map the order to the order item. And we used the
    foreign key to map the product to the order item.
    """

    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    date_created = models.DateField(default=datetime.datetime.today)


class Cart(models.Model):
    """Cart Model

    The Cart model is used to map the cart to the database. This model is used
    to create, update and delete a cart. In this model we used the foreign key
    to map the user to the cart. And we used the foreign key to map the product
    to the cart.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, blank=False)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
>>>>>>> f2553bb (Add product api in authentication app)
