from django.contrib.auth import get_user_model
from rest_framework import serializers
from api.presence import is_user_online
from rest_framework import serializers
from .models import Message

class UserWithStatusSerializer(serializers.ModelSerializer):
    is_online = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'is_online', 'avatar']

    def get_is_online(self, obj):
        return True if is_user_online(obj.id) == 1 else False

    def get_avatar(self, obj):
        return ''


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'text', 'timestamp']
