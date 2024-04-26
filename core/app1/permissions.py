# permissions.py

from rest_framework.permissions import BasePermission

class IsTaskOwner(BasePermission):
    """
    Custom permission to only allow owners of a task to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user making the request is the owner of the task
        return obj.assigned_user == request.user
