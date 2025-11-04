import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone


class Streak(models.Model):
    """Track user daily activity streaks"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='streak')
    
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
    
    total_logins = models.IntegerField(default=0)
    total_applications = models.IntegerField(default=0)
    total_profile_updates = models.IntegerField(default=0)
    total_jobs_saved = models.IntegerField(default=0)
    total_jobs_viewed = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-current_streak']
    
    def __str__(self):
        return f"{self.user.name} - {self.current_streak} day streak"
    
    def check_and_update_streak(self):
        """Check if streak should be updated or reset"""
        today = timezone.now().date()
        
        if not self.last_activity_date:
            # First activity
            self.current_streak = 1
            self.last_activity_date = today
            if self.current_streak > self.longest_streak:
                self.longest_streak = self.current_streak
            self.save()
            return True
        
        days_diff = (today - self.last_activity_date).days
        
        if days_diff == 0:
            # Same day, no change
            return False
        elif days_diff == 1:
            # Consecutive day, increment streak
            self.current_streak += 1
            self.last_activity_date = today
            if self.current_streak > self.longest_streak:
                self.longest_streak = self.current_streak
            self.save()
            return True
        else:
            # Streak broken, reset to 1
            self.current_streak = 1
            self.last_activity_date = today
            self.save()
            return True


class Achievement(models.Model):
    """Define achievements that users can earn"""
    
    ACHIEVEMENT_TYPE_CHOICES = [
        ('streak', 'Streak'),
        ('applications', 'Applications'),
        ('profile', 'Profile'),
        ('social', 'Social'),
        ('milestone', 'Milestone'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    achievement_type = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPE_CHOICES)
    
    icon = models.CharField(max_length=50, default='🏆')  # Emoji or icon name
    points_reward = models.IntegerField(default=0)
    
    # Criteria
    requirement_type = models.CharField(max_length=50)  # 'streak_days', 'total_applications', etc.
    requirement_value = models.IntegerField()
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['achievement_type', 'requirement_value']
    
    def __str__(self):
        return f"{self.icon} {self.name}"


class UserAchievement(models.Model):
    """Track achievements earned by users"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'achievement']
        ordering = ['-earned_at']
    
    def __str__(self):
        return f"{self.user.name} earned {self.achievement.name}"


class PointsHistory(models.Model):
    """Track all points earned/spent by users"""
    
    ACTION_CHOICES = [
        ('login', 'Daily Login'),
        ('application', 'Job Application'),
        ('profile_update', 'Profile Update'),
        ('streak_milestone', 'Streak Milestone'),
        ('achievement', 'Achievement Earned'),
        ('job_saved', 'Job Saved'),
        ('job_viewed', 'Job Viewed'),
        ('referral', 'Referral'),
        ('bonus', 'Bonus'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='points_history')
    
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    points = models.IntegerField()
    description = models.CharField(max_length=255)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Points History'
    
    def __str__(self):
        return f"{self.user.name} - {self.action}: {self.points} pts"


class Leaderboard(models.Model):
    """Cache for leaderboard rankings"""
    
    PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('all_time', 'All Time'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leaderboard_entries')
    
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES)
    rank = models.IntegerField()
    points = models.IntegerField()
    
    period_start = models.DateField()
    period_end = models.DateField()
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'period', 'period_start']
        ordering = ['period', 'rank']
    
    def __str__(self):
        return f"#{self.rank} {self.user.name} - {self.period}"
