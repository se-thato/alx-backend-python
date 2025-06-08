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
        fields = "__all__" 

    def get_participants_count(self, obj):
        return obj.participants.count()

        

class MessageSerializer(serializers.ModelSerializer):
    extra_text = serializers.CharField(required=False, allow_blank=True, max_length=255)

    
    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ['message_id', 'sent_at']

        def validate_message_body(self, value):
            if not value.strip():
                raise serializers.ValidationError("Message body cannot be empty.")
            return value

