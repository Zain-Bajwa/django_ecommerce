"""Serializers for the Product APIs

This file contains all the serializers for the Product APIs. The
CategorySerializer is used to create the category. The AllCategorySerializer is
used to format the all the categories data into json format. The
ProductSerializer is used to create the product and so on.
"""

from rest_framework.serializers import ModelSerializer
from core.models import (
    Cart, Category, Order, OrderItem, Product, ProductReview
)


class CategoryViewSerializer(ModelSerializer):
    """Category View Serializer

    This class is used to format the category data. The category data is
    returned in a json format including the category id and name.
    """

    class Meta:
        """Meta class for the Category View Serializer"""

        model = Category
        fields = ["id", "name"]


class ProductViewSerializer(ModelSerializer):
    """Product View Serializer

    This class is used to format the product data. The product data is
    returned in a json format including the product id, name, price, category,
    stock, sold and description.
    """

    class Meta:
        """Meta class for the ProductViewSerializer"""

        model = Product
        fields = [
            "id",
            "name",
            "price",
            "category",
            "stock",
            "sold",
            "description",
            "image",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["category"] = CategoryViewSerializer(
            instance.category
        ).data.get("name")
        return representation


class ReviewSerializer(ModelSerializer):
    """Review Serializer

    This serializer is used set the data format for Review Model
    """
    class Meta:
        """Meta class for the ProductReview Serializer"""
        model = ProductReview
        fields = ['product', 'user', 'review', 'rating']
        REQUIRED_FIELD = ['product', 'user']


class CartSerializer(ModelSerializer):
    """Cart Serializer

    This class is used to format the cart data. The cart data is returned in a
    json format including the cart id, customer and products.
    """

    class Meta:
        """Meta class for the Cart Serializer"""

        model = Cart
        fields = ["user", "product", "quantity", "price"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["product"] = ProductViewSerializer(
            instance.product
        ).data
        representation["user"] = {
            "id": instance.user.id,
            "name": instance.user.username,
        }
        return representation


class OrderSerializer(ModelSerializer):
    """Order Serializer

    This class is used to format the order data. The order data is returned in
    a json format including the order id, user, price, address, phone number
    and date_created.
    """

    class Meta:
        """Meta class for the OrderSerializer"""

        model = Order
        fields = ["user", "price", "address", "phone", "date_created"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["user"] = {
            "id": instance.user.id,
            "name": instance.user.username,
        }

        return representation


class OrderDetailSerializer(ModelSerializer):
    """Place Order Serializer

    This class is used to format the place order data. The place order data is
    returned in a json format including the order id and products' detalis.
    """

    class Meta:
        """Meta class for the OrderDetailSerializer"""

        model = OrderItem
        fields = ["order", "product", "quantity", "price", "date_created"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["order"] = OrderSerializer(instance.order).data
        representation["product"] = ProductViewSerializer(
            instance.product
        ).data
        return representation
