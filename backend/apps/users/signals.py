"""
Signals for User App
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, JobAlertPreference


@receiver(post_save, sender=User)
def create_job_alert_preference(sender, instance, created, **kwargs):
    """
    Create JobAlertPreference when a new user is created
    """
    if created:
        JobAlertPreference.objects.get_or_create(user=instance)
