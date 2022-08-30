""" All Views of the Authentication Application

This file contains all the views of the authentication Application. The views
are used to create, update, delete and list the users. This file also contains
a custom permission class that is used to check if the user is related to the
that Toekn.
"""

from rest_framework import generics, permissions, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.mixins import (DestroyModelMixin, ListModelMixin,
                                   RetrieveModelMixin, UpdateModelMixin)
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from .serializers import UserRegisterSerializer, UserViewSerializer, CreateTokneSerialzer
from .models import User

class UserRegisterView(generics.GenericAPIView):
    """User Registration View

    This view is used to create a new user. The user is created using the
    GenericAPIView class. The serializer is used to validate the data. The user
    is created and the data is returned.
    """
    serializer_class = UserRegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        user_data = serializer.data

        return Response(user_data, status=status.HTTP_201_CREATED)


class OwnProfilePermission(permissions.BasePermission):
    """Custom Permission Class

    This class is used to check if the user is related to his token. This class
    is used in the UserViewSet class. This clis inherited from the
    BasePermission to connect to the has_permission method.
    """

    def has_permission(self, request, view):
        """Override has_permission method"""
        return request.user == User.objects.get(pk=view.kwargs['pk'])


class UserViewSet(viewsets.GenericViewSet, RetrieveModelMixin,
                UpdateModelMixin, DestroyModelMixin):
    """User ViewSet
    This viewset is used to retrieve, update and delete a user. In this class
    JWT authentication is used to authenticate the user. This class also uses
    the OwnProfilePermission class to check if the user is related to his
    token.
    """

    queryset = User.objects.all()

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, OwnProfilePermission]
    serializer_class = UserViewSerializer
    lookup_field = 'pk'


class AllUserViewSet(viewsets.GenericViewSet, ListModelMixin):
    """All User ViewSet
    This viewset is used to retrieve all the users. This class uses the JWT
    authentcation to authenticate the user.
    """

    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserViewSerializer


class CreateTokenView(TokenViewBase):
    """Create Token View

    This view is used to create a new token. This is inherited from the
    TokenViewBase of the rest_framework_simplejwt.views. The purpose of this
    view is to create a new token and override the default_error_message.
    """

    serializer_class = CreateTokneSerialzer
