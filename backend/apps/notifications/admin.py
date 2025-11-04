from django.contrib import admin
from .models import Notification, PushNotificationToken, NotificationPreference


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'notification_type', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['recipient__email', 'recipient__name', 'title', 'message']
    readonly_fields = ['id', 'created_at', 'read_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('recipient', 'notification_type', 'title', 'message')
        }),
        ('Additional Data', {
            'fields': ('data', 'action_url')
        }),
        ('Status', {
            'fields': ('is_read', 'read_at', 'created_at')
        }),
    )


@admin.register(PushNotificationToken)
class PushNotificationTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'device_type', 'device_name', 'is_active', 'last_used_at']
    list_filter = ['device_type', 'is_active', 'created_at']
    search_fields = ['user__email', 'user__name', 'token', 'device_name']
    readonly_fields = ['id', 'created_at', 'updated_at', 'last_used_at']


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_application_updates', 'push_application_updates', 'updated_at']
    search_fields = ['user__email', 'user__name']
    readonly_fields = ['id', 'updated_at']
    
    fieldsets = (
        ('Email Notifications', {
            'fields': ('email_application_updates', 'email_new_jobs', 
                      'email_achievements', 'email_reminders', 'email_marketing')
        }),
        ('Push Notifications', {
            'fields': ('push_application_updates', 'push_new_jobs', 
                      'push_achievements', 'push_reminders')
        }),
        ('In-App Notifications', {
            'fields': ('inapp_application_updates', 'inapp_new_jobs', 
                      'inapp_achievements', 'inapp_reminders')
        }),
    )
