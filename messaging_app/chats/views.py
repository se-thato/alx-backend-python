from django.shortcuts import render
from .serializers import ConversationSerializer, MessageSerializer
from .models import Conversation, Message
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response



class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]



class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]


