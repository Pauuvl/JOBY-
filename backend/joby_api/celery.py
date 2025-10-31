"""
Celery configuration for background tasks and scheduled notifications
"""
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'joby_api.settings')

app = Celery('joby_api')

# Load config from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()

# Celery Beat Schedule for periodic tasks
app.conf.beat_schedule = {
    # Send daily streak reminders at 8 PM
    'send-streak-reminders': {
        'task': 'apps.notifications.tasks.send_streak_reminders',
        'schedule': crontab(hour=20, minute=0),  # 8:00 PM daily
    },
    # Check for new job recommendations every 6 hours
    'check-new-job-recommendations': {
        'task': 'apps.notifications.tasks.check_new_job_recommendations',
        'schedule': crontab(minute=0, hour='*/6'),  # Every 6 hours
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
