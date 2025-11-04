"""
Celery tasks for sending notifications
"""
from celery import shared_task
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_streak_reminders():
    """
    Envía recordatorios a usuarios que no han completado el reto del día.
    Se ejecuta diariamente a las 8:00 PM.
    """
    from apps.users.models import User
    from apps.streaks.models import Streak
    from apps.notifications.models import Notification, NotificationPreference
    
    today = timezone.now().date()
    
    # Obtener usuarios activos que tienen preferencias de recordatorios activadas
    users_to_notify = User.objects.filter(
        is_active=True,
        notification_preferences__push_reminders=True
    ).select_related('streak', 'notification_preferences')
    
    notifications_sent = 0
    
    for user in users_to_notify:
        try:
            # Verificar si el usuario ya completó el reto hoy
            streak = user.streak
            
            # Si no hay actividad hoy, enviar recordatorio
            if not streak.last_activity_date or streak.last_activity_date < today:
                # Crear notificación in-app
                Notification.objects.create(
                    recipient=user,
                    notification_type='reminder',
                    title='¡No olvides tu reto del día! 🔥',
                    message=f'Tienes una racha de {streak.current_streak} días. ¡No la pierdas! Completa tu reto diario ahora.',
                    data={
                        'current_streak': streak.current_streak,
                        'type': 'daily_streak_reminder'
                    },
                    action_url='/streak'
                )
                
                # TODO: Enviar push notification si hay token FCM disponible
                # send_push_notification.delay(user.id, 'daily_streak_reminder')
                
                notifications_sent += 1
                logger.info(f"Streak reminder sent to {user.email}")
                
        except Exception as e:
            logger.error(f"Error sending streak reminder to {user.email}: {str(e)}")
    
    logger.info(f"Streak reminders task completed. {notifications_sent} notifications sent.")
    return f"Sent {notifications_sent} streak reminders"


@shared_task
def check_new_job_recommendations():
    """
    Verifica nuevos trabajos que coincidan con los perfiles de usuarios
    y envía notificaciones.
    Se ejecuta cada 6 horas.
    """
    from apps.users.models import User
    from apps.jobs.models import Job
    from apps.notifications.models import Notification, NotificationPreference
    
    # Obtener trabajos publicados en las últimas 6 horas
    six_hours_ago = timezone.now() - timedelta(hours=6)
    new_jobs = Job.objects.filter(
        posted_date__gte=six_hours_ago,
        status='open'
    )
    
    if not new_jobs.exists():
        logger.info("No new jobs found in the last 6 hours.")
        return "No new jobs to notify"
    
    # Obtener usuarios activos con notificaciones de nuevos trabajos activadas
    users_to_notify = User.objects.filter(
        is_active=True,
        notification_preferences__push_new_jobs=True
    ).select_related('notification_preferences')
    
    notifications_sent = 0
    
    for user in users_to_notify:
        try:
            # TODO: Implementar lógica de matching basada en skills del usuario
            # Por ahora, notificar sobre los trabajos más recientes
            
            job_count = new_jobs.count()
            
            if job_count > 0:
                # Crear notificación in-app
                Notification.objects.create(
                    recipient=user,
                    notification_type='new_job',
                    title=f'¡{job_count} nuevo{"s" if job_count > 1 else ""} trabajo{"s" if job_count > 1 else ""}! 💼',
                    message=f'Hay {job_count} nuevo{"s" if job_count > 1 else ""} trabajo{"s" if job_count > 1 else ""} que podrían interesarte.',
                    data={
                        'job_count': job_count,
                        'type': 'new_jobs_available'
                    },
                    action_url='/jobs'
                )
                
                notifications_sent += 1
                logger.info(f"New job notification sent to {user.email}")
                
        except Exception as e:
            logger.error(f"Error sending job notification to {user.email}: {str(e)}")
    
    logger.info(f"New job notifications task completed. {notifications_sent} notifications sent.")
    return f"Sent {notifications_sent} new job notifications"


@shared_task
def send_achievement_notification(user_id, achievement_id):
    """
    Envía notificación cuando un usuario desbloquea un logro.
    """
    from apps.users.models import User
    from apps.streaks.models import Achievement
    from apps.notifications.models import Notification
    
    try:
        user = User.objects.get(id=user_id)
        achievement = Achievement.objects.get(id=achievement_id)
        
        # Crear notificación in-app
        Notification.objects.create(
            recipient=user,
            notification_type='achievement',
            title=f'¡Logro desbloqueado! {achievement.icon}',
            message=f'Has desbloqueado "{achievement.name}". +{achievement.points_reward} puntos',
            data={
                'achievement_id': str(achievement.id),
                'achievement_name': achievement.name,
                'points_reward': achievement.points_reward,
                'type': 'achievement_unlocked'
            },
            action_url='/profile/achievements'
        )
        
        # TODO: Enviar push notification
        # send_push_notification.delay(user.id, 'achievement_unlocked', achievement.id)
        
        logger.info(f"Achievement notification sent to {user.email} for {achievement.name}")
        return f"Achievement notification sent to {user.email}"
        
    except Exception as e:
        logger.error(f"Error sending achievement notification: {str(e)}")
        return f"Error: {str(e)}"


@shared_task
def send_application_status_notification(user_id, application_id, new_status):
    """
    Envía notificación cuando cambia el estado de una aplicación.
    """
    from apps.users.models import User
    from apps.applications.models import Application
    from apps.notifications.models import Notification
    
    try:
        user = User.objects.get(id=user_id)
        application = Application.objects.select_related('job').get(id=application_id)
        
        status_messages = {
            'pending': 'Tu aplicación está siendo revisada',
            'reviewing': 'Tu aplicación está en proceso de revisión',
            'interview': '¡Felicidades! Has sido seleccionado para una entrevista',
            'accepted': '¡Excelente noticia! Tu aplicación fue aceptada',
            'rejected': 'Gracias por aplicar. Lamentablemente no fuiste seleccionado esta vez',
        }
        
        message = status_messages.get(new_status, 'El estado de tu aplicación ha cambiado')
        
        # Crear notificación in-app
        Notification.objects.create(
            recipient=user,
            notification_type='application_status',
            title=f'Actualización: {application.job.title}',
            message=message,
            data={
                'application_id': str(application.id),
                'job_id': str(application.job.id),
                'job_title': application.job.title,
                'new_status': new_status,
                'type': 'application_status_update'
            },
            action_url=f'/applications/{application.id}'
        )
        
        # TODO: Enviar push notification
        # send_push_notification.delay(user.id, 'application_status_update', application.id)
        
        logger.info(f"Application status notification sent to {user.email}")
        return f"Application status notification sent to {user.email}"
        
    except Exception as e:
        logger.error(f"Error sending application status notification: {str(e)}")
        return f"Error: {str(e)}"


@shared_task
def send_streak_milestone_notification(user_id, streak_days):
    """
    Envía notificación cuando el usuario alcanza un hito de racha (7, 14, 30, 60, 90 días).
    """
    from apps.users.models import User
    from apps.notifications.models import Notification
    
    milestone_messages = {
        7: ('¡Una semana completa! 🎉', '¡Increíble! Has mantenido tu racha por 7 días seguidos'),
        14: ('¡Dos semanas! 🌟', '¡Vas súper bien! 14 días de racha consecutiva'),
        30: ('¡Un mes completo! 🏆', '¡Eres imparable! 30 días de racha, ¡sigue así!'),
        60: ('¡Dos meses! 💪', '¡Wow! 60 días de racha. Eres un verdadero campeón'),
        90: ('¡Tres meses! 👑', '¡Legendario! 90 días de racha consecutiva. ¡Eres increíble!'),
        100: ('¡100 días! 🎊', '¡ÉPICO! Has alcanzado 100 días de racha. ¡Felicitaciones!'),
    }
    
    if streak_days not in milestone_messages:
        return f"No milestone for {streak_days} days"
    
    try:
        user = User.objects.get(id=user_id)
        title, message = milestone_messages[streak_days]
        
        # Crear notificación in-app
        Notification.objects.create(
            recipient=user,
            notification_type='streak',
            title=title,
            message=message,
            data={
                'streak_days': streak_days,
                'type': 'streak_milestone'
            },
            action_url='/streak'
        )
        
        # TODO: Enviar push notification
        # send_push_notification.delay(user.id, 'streak_milestone', streak_days)
        
        logger.info(f"Streak milestone notification sent to {user.email} for {streak_days} days")
        return f"Streak milestone notification sent to {user.email}"
        
    except Exception as e:
        logger.error(f"Error sending streak milestone notification: {str(e)}")
        return f"Error: {str(e)}"


@shared_task
def send_challenge_completion_notification(user_id, user_challenge_id):
    """
    Envía notificación cuando un usuario completa un reto.
    """
    from apps.users.models import User
    from apps.streaks.models import UserChallenge
    from apps.notifications.models import Notification
    
    try:
        user = User.objects.get(id=user_id)
        user_challenge = UserChallenge.objects.select_related('challenge').get(id=user_challenge_id)
        challenge = user_challenge.challenge
        
        # Crear notificación in-app
        Notification.objects.create(
            recipient=user,
            notification_type='achievement',
            title=f'¡Reto completado! {challenge.icon}',
            message=f'Has completado "{challenge.title}". +{user_challenge.points_earned} puntos',
            data={
                'challenge_id': str(challenge.id),
                'challenge_title': challenge.title,
                'points_earned': user_challenge.points_earned,
                'type': 'challenge_completed'
            },
            action_url='/streak'
        )
        
        # TODO: Enviar push notification
        # send_push_notification.delay(user.id, 'challenge_completed', user_challenge.id)
        
        logger.info(f"Challenge completion notification sent to {user.email} for {challenge.title}")
        return f"Challenge completion notification sent to {user.email}"
        
    except Exception as e:
        logger.error(f"Error sending challenge completion notification: {str(e)}")
        return f"Error: {str(e)}"


# TODO: Implementar envío de push notifications con Firebase Cloud Messaging
@shared_task
def send_push_notification(user_id, notification_type, data=None):
    """
    Envía una push notification a través de Firebase Cloud Messaging.
    Requiere configuración de Firebase.
    """
    # Implementar cuando Firebase esté configurado
    pass
