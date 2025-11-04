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
        ('challenge_completed', 'Challenge Completed'),
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


class Challenge(models.Model):
    """Retos diarios y semanales para usuarios"""
    
    TYPE_CHOICES = [
        ('daily', 'Reto Diario'),
        ('weekly', 'Reto Semanal'),
        ('special', 'Reto Especial'),
    ]
    
    CATEGORY_CHOICES = [
        ('applications', 'Aplicaciones'),
        ('profile', 'Perfil'),
        ('learning', 'Aprendizaje'),
        ('networking', 'Networking'),
        ('streak', 'Racha'),
        ('exploration', 'Exploración'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    title = models.CharField(max_length=200, verbose_name='Título')
    description = models.TextField(verbose_name='Descripción')
    icon = models.CharField(max_length=50, default='🎯', verbose_name='Icono')
    
    challenge_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='Tipo')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name='Categoría')
    
    # Criteria
    target_action = models.CharField(max_length=50, verbose_name='Acción objetivo', 
                                     help_text='Ej: apply_to_jobs, update_profile, view_jobs')
    target_count = models.IntegerField(default=1, verbose_name='Cantidad requerida')
    
    # Rewards
    points_reward = models.IntegerField(default=10, verbose_name='Puntos de recompensa')
    bonus_multiplier = models.DecimalField(max_digits=3, decimal_places=2, default=1.0, 
                                          verbose_name='Multiplicador de bonus')
    
    # Availability
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    start_date = models.DateField(null=True, blank=True, verbose_name='Fecha inicio')
    end_date = models.DateField(null=True, blank=True, verbose_name='Fecha fin')
    
    # Priority (para mostrar en orden)
    priority = models.IntegerField(default=0, verbose_name='Prioridad')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'challenges'
        ordering = ['-priority', '-created_at']
        verbose_name = 'Reto'
        verbose_name_plural = 'Retos'
    
    def __str__(self):
        return f"{self.icon} {self.title} ({self.get_challenge_type_display()})"
    
    def is_available(self):
        """Check if challenge is currently available"""
        today = timezone.now().date()
        
        if not self.is_active:
            return False
        
        if self.start_date and today < self.start_date:
            return False
        
        if self.end_date and today > self.end_date:
            return False
        
        return True


class UserChallenge(models.Model):
    """Track user progress on challenges"""
    
    STATUS_CHOICES = [
        ('active', 'Activo'),
        ('completed', 'Completado'),
        ('expired', 'Expirado'),
        ('abandoned', 'Abandonado'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_challenges')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='user_progress')
    
    # Progress tracking
    current_progress = models.IntegerField(default=0, verbose_name='Progreso actual')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='Estado')
    
    # Dates
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    # Rewards given
    points_earned = models.IntegerField(default=0, verbose_name='Puntos ganados')
    
    class Meta:
        db_table = 'user_challenges'
        unique_together = ['user', 'challenge', 'started_at']
        ordering = ['-started_at']
        verbose_name = 'Reto de Usuario'
        verbose_name_plural = 'Retos de Usuarios'
        indexes = [
            models.Index(fields=['user', 'status', '-started_at']),
        ]
    
    def __str__(self):
        return f"{self.user.name} - {self.challenge.title} ({self.status})"
    
    @property
    def progress_percentage(self):
        """Calculate progress percentage"""
        if self.challenge.target_count == 0:
            return 0
        return min(int((self.current_progress / self.challenge.target_count) * 100), 100)
    
    @property
    def is_completed(self):
        """Check if challenge is completed"""
        return self.current_progress >= self.challenge.target_count
    
    def update_progress(self, increment=1):
        """Update challenge progress"""
        self.current_progress += increment
        
        # Check if completed
        if self.is_completed and self.status != 'completed':
            self.complete_challenge()
        else:
            self.save()
    
    def complete_challenge(self):
        """Mark challenge as completed and award points"""
        from apps.streaks.services import StreakService
        
        if self.status == 'completed':
            return  # Already completed
        
        self.status = 'completed'
        self.completed_at = timezone.now()
        
        # Calculate points with bonus multiplier
        base_points = self.challenge.points_reward
        bonus_points = int(base_points * float(self.challenge.bonus_multiplier - 1))
        total_points = base_points + bonus_points
        
        self.points_earned = total_points
        self.save()
        
        # Award points to user
        StreakService.award_points(
            self.user,
            'challenge_completed',
            total_points,
            f"Reto completado: {self.challenge.title}"
        )
        
        # Send notification
        from apps.notifications.tasks import send_challenge_completion_notification
        send_challenge_completion_notification.delay(str(self.user.id), str(self.id))
        
        return total_points
