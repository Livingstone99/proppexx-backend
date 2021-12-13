
from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response


class IsAgent(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.user_type == 'agent')


class IsBuyer(BasePermission):
    message = 'only buyers are allowed'

    def has_permission(self, request, view):
        try:
            if request.user.user_type == 'buyer':
                return True
        except:
            return False

class IsDeveloper(BasePermission):
    message = 'only developers are allowed'

    def has_permission(self, request, view):
        if request.user.user_type == 'developer':
            return True


class IsAgentOrAdmin(BasePermission):
    message = 'Only Admin and Agents are Allowed'

    def has_permission(self, request, view):
        if request.user.user_type == 'agent' or request.user.is_staff:
            return True


class IsAgentOrDeveloper(BasePermission):
    message = 'Only Developer and Agents are Allowed'

    def has_permission(self, request, view):
        if request.user.user_type == 'agent' or request.user.user_type == 'developer':
            return True


class IsAgentOrDeveloperOrAdmin(BasePermission):
    message = 'Only Developer, Admin and Agents are Allowed'

    def has_permission(self, request, view):
        if request.user.user_type == 'agent' or request.user.user_type == 'developer' or request.user.is_staff:
            return True
        else:
            return False
