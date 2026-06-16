from rest_framework import permissions


class ReadOnlyOrAdminMutations(permissions.BasePermission):
    """
    Allows read-only access to anyone,
    but requires staff status for any write operations.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
