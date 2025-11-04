from django.conf import settings
from .models import Notification, PushNotificationToken


class NotificationService:
    """Service for sending notifications"""
    
    @staticmethod
    def create_notification(recipient, notification_type, title, message, data=None, action_url=''):
        """Create an in-app notification"""
        notification = Notification.objects.create(
            recipient=recipient,
            notification_type=notification_type,
            title=title,
            message=message,
            data=data or {},
            action_url=action_url
        )
        
        # Send push notification if enabled
        NotificationService.send_push_notification(
            recipient,
            notification_type,
            title,
            message,
            data
        )
        
        return notification
    
    @staticmethod
    def send_push_notification(user, notification_type, title, message, data=None):
        """Send push notification via Firebase FCM"""
        try:
            # Check user preferences
            prefs = getattr(user, 'notification_preferences', None)
            if not prefs:
                return False
            
            # Check if push notifications are enabled for this type
            push_enabled = False
            if notification_type == 'application_status':
                push_enabled = prefs.push_application_updates
            elif notification_type == 'new_job':
                push_enabled = prefs.push_new_jobs
            elif notification_type in ['achievement', 'streak']:
                push_enabled = prefs.push_achievements
            elif notification_type == 'reminder':
                push_enabled = prefs.push_reminders
            
            if not push_enabled:
                return False
            
            # Get active FCM tokens
            tokens = PushNotificationToken.objects.filter(
                user=user,
                is_active=True
            ).values_list('token', flat=True)
            
            if not tokens:
                return False
            
            # Send via Firebase (commented out - requires Firebase setup)
            # from firebase_admin import messaging
            # 
            # messages = [
            #     messaging.Message(
            #         notification=messaging.Notification(
            #             title=title,
            #             body=message
            #         ),
            #         data=data or {},
            #         token=token
            #     )
            #     for token in tokens
            # ]
            # 
            # response = messaging.send_all(messages)
            # return response.success_count > 0
            
            # For now, just return True (Firebase not configured)
            return True
            
        except Exception as e:
            print(f"Error sending push notification: {e}")
            return False
    
    @staticmethod
    def send_application_status_notification(application):
        """Send notification when application status changes"""
        user = application.applicant
        job = application.job
        
        status_messages = {
            'reviewed': 'Your application is being reviewed',
            'interview': 'You have been invited for an interview!',
            'offered': 'Congratulations! You received a job offer!',
            'accepted': 'Your application has been accepted',
            'rejected': 'Your application status has been updated'
        }
        
        message = status_messages.get(application.status, 'Your application status has been updated')
        
        return NotificationService.create_notification(
            recipient=user,
            notification_type='application_status',
            title=f'Application Update: {job.title}',
            message=message,
            data={
                'application_id': str(application.id),
                'job_id': str(job.id),
                'status': application.status
            },
            action_url=f'/applications/{application.id}'
        )
    
    @staticmethod
    def send_new_job_notification(user, job):
        """Send notification for new job matching user profile"""
        return NotificationService.create_notification(
            recipient=user,
            notification_type='new_job',
            title='New Job Match!',
            message=f'Check out this new opportunity: {job.title} at {job.company_name}',
            data={
                'job_id': str(job.id),
                'company': job.company_name
            },
            action_url=f'/jobs/{job.id}'
        )
    
    @staticmethod
    def send_achievement_notification(user, achievement):
        """Send notification when user earns achievement"""
        return NotificationService.create_notification(
            recipient=user,
            notification_type='achievement',
            title='🏆 Achievement Unlocked!',
            message=f'Congratulations! You earned "{achievement.name}"',
            data={
                'achievement_id': str(achievement.id),
                'points_reward': achievement.points_reward
            },
            action_url='/profile/achievements'
        )
    
    @staticmethod
    def send_streak_milestone_notification(user, streak_days):
        """Send notification for streak milestone"""
        return NotificationService.create_notification(
            recipient=user,
            notification_type='streak',
            title='🔥 Streak Milestone!',
            message=f'Amazing! You have a {streak_days}-day streak!',
            data={
                'streak_days': streak_days
            },
            action_url='/profile/stats'
        )
    
    @staticmethod
    def send_reminder_notification(user, title, message, action_url=''):
        """Send a reminder notification"""
        return NotificationService.create_notification(
            recipient=user,
            notification_type='reminder',
            title=title,
            message=message,
            action_url=action_url
        )
