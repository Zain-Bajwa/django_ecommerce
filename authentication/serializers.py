"""Serializers for the authentication Application

This file contains all the serializers for the authentication Application. The
RegisterSerializers is used to create the user. The UserViewSerializer is used
to format the user profile data into json format. The AllUserViewSerializer is
used to format the all the users data into json format.
"""

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


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
