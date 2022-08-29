"""Serializers for the authentication Application

This file contains all the serializers for the authentication Application. The
RegisterSerializers is used to create the user. The UserViewSerializer is used
to format the user profile data into json format. The CategorySerializer
is used to create the category. The AllCategorySerializer is used to format the
all the categories data into json format. The ProductSerializer is used to
create the product and so on.
"""

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Cart, Category, Order, OrderItem, Product, User


# pylint: disable=too-few-public-methods
class UserRegisterSerializer(serializers.ModelSerializer):
    """User Register Serializer

    In this class we override the method creat to create extend user. The user
    is created using the create method from the User model. The password is set
    using the set_password method from the User model to encrypt the password.
    The user is saved using the save method and returned.`
    """

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        """Meta class for the User Register Serializer"""

        model = User
        fields = ["id", "username", "password", "confirm_password"]
        read_only = ["confirm_password"]

    def validate(self, attrs):
        """Validate the password and confirm password

        This method is used to validate the password and confirm password. If
        the password and confirm password are not same then raise an error.
        This method is also used to validate the weak password. If the password
        is weak then raise an error.
        """

        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        """Create the user

        This method is used to create the user. The user is created using the
        create method from the User model. The password is set using the
        set_password method from the User model to encrypt the password. The
        user is saved using the save method and returned. The user is also
        saved in the database.
        """

        user = User.objects.create(username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        return user


# pylint: disable=abstract-method
class UserViewSerializer(serializers.ModelSerializer):
    """User View Serializer

    This class is used to format the user data. The user data is returned in a
    json format including the user id, email, username, first name, last name,
    address and phone number. The user data is returned in a json format
    including the user id, email, username, first name, last name, address and
    phone number.
    """

    class Meta:
        """Meta class for the User View Serializer"""

        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "address",
            "phone_no",
        ]


class CreateTokneSerialzer(TokenObtainPairSerializer):
    """Create Token Serializer
    This class is used to create the token. The token is created using the
    TokenObtainPairSerializer class. The token is returned in a json format.
    In this class the default error message is overridden.
    """

    default_error_messages = {
                        'no_active_account': _('Invalid username/password.')
    }

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user_id"] = self.user.id
        return data


class CategoryViewSerializer(serializers.ModelSerializer):
    """Category View Serializer

    This class is used to format the category data. The category data is
    returned in a json format including the category id and name.
    """

    class Meta:
        """Meta class for the Category View Serializer"""

        model = Category
        fields = ["id", "name"]


class ProductViewSerializer(serializers.ModelSerializer):
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
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["category"] = CategoryViewSerializer(
            instance.category
        ).data.get("name")
        return representation


class CartSerializer(serializers.ModelSerializer):
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


class OrderSerializer(serializers.ModelSerializer):
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


class OrderDetailSerializer(serializers.ModelSerializer):
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
