from rest_framework.permissions import BasePermission


class NotAuthenticated(BasePermission):
    """
    Simple permission class to check if user isn't authenticated.
    """
    def has_permission(self, request, view):
        return not bool(request.user.is_authenticated)
