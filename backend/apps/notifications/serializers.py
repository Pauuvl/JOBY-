from rest_framework import serializers
from .models import Notification, PushNotificationToken, NotificationPreference


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model"""
    
    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'notification_type', 'title', 'message',
            'data', 'action_url', 'is_read', 'read_at', 'created_at'
        ]
        read_only_fields = ['id', 'recipient', 'created_at']


class PushNotificationTokenSerializer(serializers.ModelSerializer):
    """Serializer for PushNotificationToken model"""
    
    class Meta:
        model = PushNotificationToken
        fields = [
            'id', 'user', 'token', 'device_type', 'device_name',
            'is_active', 'created_at', 'last_used_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'last_used_at']


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    """Serializer for NotificationPreference model"""
    
    class Meta:
        model = NotificationPreference
        fields = [
            'id', 'user', 'email_application_updates', 'email_new_jobs',
            'email_achievements', 'email_reminders', 'email_marketing',
            'push_application_updates', 'push_new_jobs', 'push_achievements',
            'push_reminders', 'inapp_application_updates', 'inapp_new_jobs',
            'inapp_achievements', 'inapp_reminders', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'updated_at']
