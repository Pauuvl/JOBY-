"""
Celery Tasks for Job Alerts
"""
from celery import shared_task
from django.utils import timezone
from .models import User, JobAlertPreference


@shared_task
def check_job_alerts_for_all_users():
    """
    Check job alerts for all users with enabled preferences
    This task should run periodically (e.g., every hour)
    """
    from apps.jobs.services import JobMatchingService
    
    # Get users with enabled alerts
    preferences = JobAlertPreference.objects.filter(is_enabled=True).select_related('user')
    
    alerts_sent = 0
    for preference in preferences:
        try:
            notification = JobMatchingService.check_new_jobs_for_user(preference.user)
            if notification:
                alerts_sent += 1
        except Exception as e:
            print(f"Error checking alerts for user {preference.user.email}: {str(e)}")
    
    return f"Checked {preferences.count()} users, sent {alerts_sent} alerts"


@shared_task
def send_daily_job_digest():
    """
    Send daily digest of matching jobs to users with daily frequency
    """
    from apps.jobs.services import JobMatchingService
    
    # Get users with daily frequency
    preferences = JobAlertPreference.objects.filter(
        is_enabled=True,
        frequency='daily'
    ).select_related('user')
    
    digests_sent = 0
    for preference in preferences:
        try:
            # Find matching jobs
            matching_jobs = JobMatchingService.find_matching_jobs(preference.user, min_score=60)
            
            if matching_jobs:
                JobMatchingService.send_job_alert(preference.user, matching_jobs)
                digests_sent += 1
        except Exception as e:
            print(f"Error sending digest to user {preference.user.email}: {str(e)}")
    
    return f"Sent {digests_sent} daily digests"


@shared_task
def send_weekly_job_digest():
    """
    Send weekly digest of matching jobs to users with weekly frequency
    """
    from apps.jobs.services import JobMatchingService
    
    # Get users with weekly frequency
    preferences = JobAlertPreference.objects.filter(
        is_enabled=True,
        frequency='weekly'
    ).select_related('user')
    
    digests_sent = 0
    for preference in preferences:
        try:
            # Find matching jobs
            matching_jobs = JobMatchingService.find_matching_jobs(preference.user, min_score=60)
            
            if matching_jobs:
                JobMatchingService.send_job_alert(preference.user, matching_jobs)
                digests_sent += 1
        except Exception as e:
            print(f"Error sending digest to user {preference.user.email}: {str(e)}")
    
    return f"Sent {digests_sent} weekly digests"
