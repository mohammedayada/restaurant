from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Global permission check for user is admin.
    """

    def has_permission(self, request, view):
        if request.user.role == 'Admin':
            return True
        else:
            return False
