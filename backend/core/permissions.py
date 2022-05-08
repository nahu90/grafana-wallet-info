from core.services import user_service
from rest_framework import permissions


class IsSysAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if user_service.is_admin(request.user):
            return True
        return False
