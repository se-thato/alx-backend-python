from django.shortcuts import render
from .serializers import ConversationSerializer, MessageSerializer
from .models import Conversation, Message
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsParticipantOrReadOnly


#this will be used to create views for the Conversation and Message models
class ConversationViewSet(viewsets.ModelViewSet):
    """
    getting all conversations
    then serializing them
    and providing permissions for authenticated users
    """
    queryset = Conversation.objects.all() 
    serializer_class = ConversationSerializer
    permission_classes = (IsAuthenticated, IsParticipantOrReadOnly)


# this will be used to create views for the Message model
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated, IsParticipantOrReadOnly)

    #allowing filtering on the conversation field
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['conversation']  # this will allow us to filter messages by conversation


