import uuid
from django.db import models
from django.conf import settings


class Notification(models.Model):
    """In-app notifications"""
    
    NOTIFICATION_TYPE_CHOICES = [
        ('application_status', 'Application Status Update'),
        ('new_job', 'New Job Match'),
        ('achievement', 'Achievement Unlocked'),
        ('streak', 'Streak Milestone'),
        ('message', 'Message'),
        ('reminder', 'Reminder'),
        ('system', 'System Notification'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    # Optional metadata as JSON
    data = models.JSONField(default=dict, blank=True)
    
    # Action URL (optional)
    action_url = models.CharField(max_length=500, blank=True)
    
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['recipient', 'is_read', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.notification_type} for {self.recipient.name}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            from django.utils import timezone
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])


class PushNotificationToken(models.Model):
    """Store FCM tokens for push notifications"""
    
    DEVICE_TYPE_CHOICES = [
        ('ios', 'iOS'),
        ('android', 'Android'),
        ('web', 'Web'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='push_tokens')
    
    token = models.CharField(max_length=500, unique=True)
    device_type = models.CharField(max_length=10, choices=DEVICE_TYPE_CHOICES)
    device_name = models.CharField(max_length=200, blank=True)
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_used_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-last_used_at']
    
    def __str__(self):
        return f"{self.user.name} - {self.device_type} ({self.token[:20]}...)"


class NotificationPreference(models.Model):
    """User notification preferences"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_preferences')
    
    # Email notifications
    email_application_updates = models.BooleanField(default=True)
    email_new_jobs = models.BooleanField(default=True)
    email_achievements = models.BooleanField(default=True)
    email_reminders = models.BooleanField(default=True)
    email_marketing = models.BooleanField(default=False)
    
    # Push notifications
    push_application_updates = models.BooleanField(default=True)
    push_new_jobs = models.BooleanField(default=True)
    push_achievements = models.BooleanField(default=True)
    push_reminders = models.BooleanField(default=True)
    
    # In-app notifications
    inapp_application_updates = models.BooleanField(default=True)
    inapp_new_jobs = models.BooleanField(default=True)
    inapp_achievements = models.BooleanField(default=True)
    inapp_reminders = models.BooleanField(default=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Notification preferences for {self.user.name}"
