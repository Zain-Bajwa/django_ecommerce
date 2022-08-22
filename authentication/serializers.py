"""Serializers for the authentication Application

This file contains all the serializers for the authentication Application. The
RegisterSerializers is used to create the user. The UserViewSerializer is used
to format the user profile data into json format.
"""
from rest_framework import serializers
from .models import User

class RegisterSerializers(serializers.ModelSerializer):
    """User Register Serializer
    In this class we override the method creat to create extend user. The user
    is created using the create method from the User model. The password is set
    using the set_password method from the User model. The user is saved using
    the save method.

    """
    class Meta:
        model = User
        fields = ['id' ,'email', 'username', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserViewSerializer(serializers.ModelSerializer):
    """User View Serializer
    
    This class is used to format the user data. The user data is returned in a
    json format including the user id, email, username, first name, last name,
    address and phone number.
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name',
                  'address', 'phone_no']
    