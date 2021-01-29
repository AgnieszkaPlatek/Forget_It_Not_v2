from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Permission checking if the user is the owner of the flashcard-set or flashcard.
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
