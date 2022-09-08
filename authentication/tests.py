"""Testing User API

This testing file is used to test the APIs of user. We have two tests one for
user registeration and other for getting JWT Token with username and password.
"""

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import User


class RegistrationTestCase(APITestCase):
    """TestCase for User Registeration"""

    def test_registeration(self):
        """We have a API call of POST method with username, password, and
        confirm_password fields. If user is created successfully then
        response.status_code will be 401.
        """

        data = {
            "username": "test4",
            "password": "Password@123",
            "confirm_password": "Password@123"
        }
        url = reverse('authentication:register-user')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class GetTokenTestCase(APITestCase):
    """TestCase for getting token"""

    def setUp(self):
        """Setup for user creation"""

        self.user = User.objects.create_user(
            username="test4",
            password="Password@123"
        )

    def test_get_token(self):
        """This test case is used to test the user login. If we provide correct
        username and password then we can get JWT Token with status_code 200.
        """

        data = {"username": "test4", "password": "Password@123"}
        url = reverse('authentication:create-token')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
