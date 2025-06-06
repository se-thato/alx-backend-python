from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated


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


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to participants of the conversation.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        
        # For Conversation objects
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        
        # For Message objects
        if hasattr(obj, 'conversation'):
            # Only participants can view, update, or delete messages
            if request.method in ['GET', 'PUT', 'PATCH', 'DELETE', 'POST']:
                return True
            return request.user in obj.conversation.participants.all()
        return False

