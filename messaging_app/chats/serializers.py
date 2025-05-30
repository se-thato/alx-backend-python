from rest_framework import serializers
from .models import Conversation, Message, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        #fields
        Conversation_id = serializers.CharField(source='conversation_id', read_only=True)
        created_at = serializers.DateTimeField(read_only=True)
        updated_at = serializers.DateTimeField(read_only=True)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ['message_id', 'sent_at']

