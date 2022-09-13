"""Product, ProductReview, Category, Cart, Order, OrderItem Model

Models are inherited from the Django.db.models.Model. These models are
used to create, update, delete a new product. We can also add a product to
cart. We can place an order.
"""

import datetime
from django.db import models
from authentication.models import User


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
    image = models.ImageField(upload_to="products", blank=True)


class ProductReview(models.Model):
    """ProductReview Model

    This model is used to take the review and rating from the user. This model
    has following fields:
    - product: Id of the product that is being reviewed
    - user: Id of the user that is giving the review for a specific product
    - review: A review message given by the user for specific product
    - rating: An integer value from 0 to 5 given by the user for a specific
      product
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=False, null=True)

    review = models.CharField(max_length=256, default='', blank=True)
    rating = models.IntegerField(default=0, blank=True)

    # pylint: disable=no-member
    def average_rating(self, product):
        """Average Rating of a product
        """
        all_rating = Product.objects.filter(product=product)
        rating_sum = 0
        for rating_ in all_rating:
            rating_sum += rating_.rating
        return round(rating_sum/all_rating.count())


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
