from rest_framework.permissions import BasePermission


class NotAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return not bool(request.user.is_authenticated)