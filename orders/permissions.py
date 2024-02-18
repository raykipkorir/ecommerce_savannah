from rest_framework import permissions

class CustomOrderPermission(permissions.BasePermission):
    """
    Authenticated users can create and get orders

    Admins and staff can update orders

    Only admins can delete orders

    Users CAN'T view orders created by other users except admins and staff
    """
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if request.method in ["POST", "GET"]:
                return True
            elif request.method in ["PUT", "PATCH"]:
                return request.user.is_staff

            return request.user.is_superuser
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if not (request.user.is_staff or request.user.is_superuser):
            return obj.customer == request.user
        return True


class IsAdminOrOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                return True
            return request.user and request.user.is_superuser
        else:
            return False

    def has_object_permission(self, request, view, obj):
        return request.user == obj.order.customer
