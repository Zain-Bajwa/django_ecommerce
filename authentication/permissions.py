"""Authentication Permissions

This file is used to define all permissions of user. This includes permissions
which API user can access. Two permissions are defined in this module:
- OwnProfilePermission
- IsSuperUser
"""

from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist
from .models import User


class OwnProfilePermission(permissions.BasePermission):
    """Custom Permission Class for the UserViewSet class

    This class is used to check if the user is related to his token. This class
    is used in the UserViewSet class. This class is inherited from the
    BasePermission to connect to the has_permission method.
    """

    def has_permission(self, request, view):
        """Check if the user is related to the token"""

        user_id = view.kwargs.get('pk') or view.kwargs.get("user_id") or \
            request.data.get("user") or request.query_params.get("user_id")

        try:
            return request.user == User.objects.get(pk=user_id)
        except ObjectDoesNotExist:
                return False



class IsSuperUser(permissions.BasePermission):
    """Custom Permission Class for the AllUserViewSet Class

    This class is used to check if the user is a superuser. This class is used
    in the AllUserViewSet class.
    """

    def has_permission(self, request, view):
        """Check if the user is a superuser"""

        return request.user and request.user.is_superuser
