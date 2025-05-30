from rest_framework import serializers
from .models import Conversation, Message, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"



class ConversationSerializer(serializers.ModelSerializer):
    participants_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        #fields
        Conversation_id = serializers.CharField(source='conversation_id', read_only=True)
        created_at = serializers.DateTimeField(read_only=True)
        updated_at = serializers.DateTimeField(read_only=True)

        def get_participant_count(self, obj):
            return obj.participants.count()




class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ['message_id', 'sent_at']

        def validate_message_body(self, value):
            if not value.strip():
                raise serializers.ValidationError("Message body cannot be empty.")
            return value

