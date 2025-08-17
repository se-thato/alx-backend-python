from django.shortcuts import render
from .serializers import ConversationSerializer, MessageSerializer
from .models import Conversation, Message
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsParticipantOrReadOnly, IsParticipantOfConversation
from rest_framework.exceptions import PermissionDenied

#this will be used to create views for the Conversation and Message models
class ConversationViewSet(viewsets.ModelViewSet):
    """
    getting all conversations
    then serializing them
    and providing permissions for authenticated users
    """
    queryset = Conversation.objects.all() 
    serializer_class = ConversationSerializer
    permission_classes = (IsAuthenticated, IsParticipantOrReadOnly, IsAdminUser, IsParticipantOfConversation)



# this will be used to create views for the Message model
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated, IsParticipantOrReadOnly)

    #allowing filtering on the conversation field
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['conversation']  # this will allow us to filter messages by conversation

    def get_queryset(self):
        user = self.request.user
        queryset = Message.objects.filter(conversation__participants=user)
        conversation_id = self.request.query_params.get('conversation_id')
        if conversation_id is not None:
            queryset = queryset.filter(conversation_id=conversation_id)
        return queryset
    

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get('conversation')
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant in this conversation.")
        serializer.save()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user not in instance.conversation.participants.all():
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user not in instance.conversation.participants.all():
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user not in instance.conversation.participants.all():
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

