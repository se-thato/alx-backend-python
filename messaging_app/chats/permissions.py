from rest_framework import permissions


class IsParticipantOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        # For Conversation objects
        if hasattr(obj, 'participants'):
            return user in obj.participants.all()
        # For Message objects
        if hasattr(obj, 'conversation'):
            return user in obj.conversation.participants.all()
        return False