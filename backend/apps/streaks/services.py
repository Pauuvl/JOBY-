from django.utils import timezone
from .models import Streak, Achievement, UserAchievement, PointsHistory


class StreakService:
    """Service for managing user streaks and points"""
    
    @staticmethod
    def record_activity(user, activity_type='login'):
        """Record user activity and update streak"""
        from apps.notifications.tasks import send_streak_milestone_notification
        
        streak, created = Streak.objects.get_or_create(user=user)
        
        # Get current streak before update
        old_streak = streak.current_streak
        
        # Update streak
        streak_updated = streak.check_and_update_streak()
        
        # Update activity counters
        if activity_type == 'login':
            streak.total_logins += 1
        elif activity_type == 'application':
            streak.total_applications += 1
        elif activity_type == 'profile_update':
            streak.total_profile_updates += 1
        elif activity_type == 'job_saved':
            streak.total_jobs_saved += 1
        elif activity_type == 'job_viewed':
            streak.total_jobs_viewed += 1
        
        streak.save()
        
        # Check if user reached a milestone (7, 14, 30, 60, 90, 100 days)
        if streak_updated and streak.current_streak > old_streak:
            milestones = [7, 14, 30, 60, 90, 100]
            if streak.current_streak in milestones:
                # Send milestone notification asynchronously
                send_streak_milestone_notification.delay(str(user.id), streak.current_streak)
        
        return streak_updated
    
    @staticmethod
    def award_points(user, action, points, description=None):
        """Award points to user and record in history"""
        if not description:
            description = f"Earned {points} points for {action}"
        
        # Update user points
        user.points += points
        user.save(update_fields=['points'])
        
        # Record in history
        PointsHistory.objects.create(
            user=user,
            action=action,
            points=points,
            description=description
        )
        
        # Check for achievements
        StreakService.check_achievements(user)
        
        return user.points
    
    @staticmethod
    def check_achievements(user):
        """Check if user has earned any new achievements"""
        try:
            streak = Streak.objects.get(user=user)
        except Streak.DoesNotExist:
            return []
        
        new_achievements = []
        
        # Get all active achievements
        achievements = Achievement.objects.filter(is_active=True)
        
        # Get already earned achievements
        earned_ids = UserAchievement.objects.filter(user=user).values_list('achievement_id', flat=True)
        
        for achievement in achievements:
            if achievement.id in earned_ids:
                continue
            
            # Check if user meets criteria
            earned = False
            
            if achievement.requirement_type == 'streak_days':
                earned = streak.current_streak >= achievement.requirement_value
            elif achievement.requirement_type == 'longest_streak':
                earned = streak.longest_streak >= achievement.requirement_value
            elif achievement.requirement_type == 'total_applications':
                earned = streak.total_applications >= achievement.requirement_value
            elif achievement.requirement_type == 'total_logins':
                earned = streak.total_logins >= achievement.requirement_value
            elif achievement.requirement_type == 'total_points':
                earned = user.points >= achievement.requirement_value
            
            if earned:
                from apps.notifications.tasks import send_achievement_notification
                
                # Award achievement
                UserAchievement.objects.create(
                    user=user,
                    achievement=achievement
                )
                
                # Award bonus points
                if achievement.points_reward > 0:
                    StreakService.award_points(
                        user,
                        'achievement',
                        achievement.points_reward,
                        f"Achievement unlocked: {achievement.name}"
                    )
                
                # Send achievement notification asynchronously
                send_achievement_notification.delay(str(user.id), str(achievement.id))
                
                new_achievements.append(achievement)
        
        return new_achievements
    
    @staticmethod
    def get_user_stats(user):
        """Get comprehensive user statistics"""
        try:
            streak = Streak.objects.get(user=user)
        except Streak.DoesNotExist:
            streak = Streak.objects.create(user=user)
        
        achievements = UserAchievement.objects.filter(user=user)
        recent_points = PointsHistory.objects.filter(user=user)[:10]
        
        return {
            'streak': {
                'current': streak.current_streak,
                'longest': streak.longest_streak,
                'last_activity': streak.last_activity_date,
            },
            'activity': {
                'total_logins': streak.total_logins,
                'total_applications': streak.total_applications,
                'total_profile_updates': streak.total_profile_updates,
                'total_jobs_saved': streak.total_jobs_saved,
                'total_jobs_viewed': streak.total_jobs_viewed,
            },
            'points': {
                'total': user.points,
                'recent_history': [
                    {
                        'action': p.action,
                        'points': p.points,
                        'description': p.description,
                        'date': p.created_at
                    }
                    for p in recent_points
                ]
            },
            'achievements': {
                'total': achievements.count(),
                'earned': [
                    {
                        'name': a.achievement.name,
                        'description': a.achievement.description,
                        'icon': a.achievement.icon,
                        'earned_at': a.earned_at
                    }
                    for a in achievements[:5]
                ]
            }
        }
