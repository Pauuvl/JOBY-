"""
Models for referral and points system
"""
import uuid
import random
import string
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


def generate_referral_code():
    """Generate unique 6-character referral code"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


class ReferralCode(models.Model):
    """Unique referral code for each user"""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='referral_code'
    )
    code = models.CharField(
        max_length=10,
        unique=True,
        default=generate_referral_code,
        verbose_name='Código de Referido'
    )
    total_referrals = models.IntegerField(
        default=0,
        verbose_name='Total de Referidos'
    )
    total_points_earned = models.IntegerField(
        default=0,
        verbose_name='Puntos Ganados por Referidos'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activo'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'referral_codes'
        verbose_name = 'Código de Referido'
        verbose_name_plural = 'Códigos de Referidos'
    
    def __str__(self):
        return f"{self.user.name} - {self.code}"
    
    def save(self, *args, **kwargs):
        # Ensure unique code
        while not self.code or ReferralCode.objects.filter(code=self.code).exclude(id=self.id).exists():
            self.code = generate_referral_code()
        super().save(*args, **kwargs)


class Referral(models.Model):
    """Track referred users"""
    
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('registered', 'Registrado'),
        ('profile_completed', 'Perfil Completado'),
        ('employed', 'Empleado'),
    ]
    
    referrer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='referrals_made',
        verbose_name='Referidor'
    )
    referred = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='referred_by',
        verbose_name='Referido'
    )
    referral_code = models.ForeignKey(
        ReferralCode,
        on_delete=models.CASCADE,
        related_name='referrals'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='registered'
    )
    
    # Points tracking
    registration_points_awarded = models.BooleanField(default=False)
    profile_completion_points_awarded = models.BooleanField(default=False)
    employment_points_awarded = models.BooleanField(default=False)
    
    # Metadata
    referred_at = models.DateTimeField(auto_now_add=True)
    last_milestone_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'referrals'
        verbose_name = 'Referido'
        verbose_name_plural = 'Referidos'
    
    def __str__(self):
        return f"{self.referrer.name} → {self.referred.name}"


class PointsTransaction(models.Model):
    """Track all points movements"""
    
    TRANSACTION_TYPES = [
        ('referral_register', 'Referido Registrado'),
        ('referral_profile', 'Referido Completó Perfil'),
        ('referral_employed', 'Referido Consiguió Empleo'),
        ('welcome_bonus', 'Bono de Bienvenida'),
        ('challenge_complete', 'Reto Completado'),
        ('streak_bonus', 'Bonus de Racha'),
        ('course_complete', 'Curso Completado'),
        ('redeem', 'Canje de Puntos'),
        ('admin_adjustment', 'Ajuste Administrativo'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='points_transactions'
    )
    transaction_type = models.CharField(
        max_length=30,
        choices=TRANSACTION_TYPES
    )
    points = models.IntegerField(
        verbose_name='Puntos'
    )
    description = models.CharField(
        max_length=255,
        verbose_name='Descripción'
    )
    
    # Optional reference to related objects
    related_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='points_transactions_about',
        verbose_name='Usuario Relacionado'
    )
    related_referral = models.ForeignKey(
        Referral,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='points_transactions'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'points_transactions'
        verbose_name = 'Transacción de Puntos'
        verbose_name_plural = 'Transacciones de Puntos'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.name} - {self.points} pts ({self.transaction_type})"


class Reward(models.Model):
    """Available rewards that can be redeemed with points"""
    
    REWARD_TYPES = [
        ('badge', 'Insignia'),
        ('course_discount', 'Descuento en Curso'),
        ('premium_feature', 'Feature Premium'),
        ('course_free', 'Curso Gratis'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    reward_type = models.CharField(max_length=20, choices=REWARD_TYPES)
    points_required = models.IntegerField(verbose_name='Puntos Requeridos')
    icon = models.CharField(max_length=50, default='🎁')
    is_active = models.BooleanField(default=True)
    
    # Limits
    max_redemptions_per_user = models.IntegerField(
        default=1,
        verbose_name='Máximo de Canjes por Usuario'
    )
    total_available = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Total Disponible'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'rewards'
        verbose_name = 'Recompensa'
        verbose_name_plural = 'Recompensas'
        ordering = ['points_required']
    
    def __str__(self):
        return f"{self.name} ({self.points_required} pts)"


class RewardRedemption(models.Model):
    """Track reward redemptions"""
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reward_redemptions'
    )
    reward = models.ForeignKey(
        Reward,
        on_delete=models.CASCADE,
        related_name='redemptions'
    )
    points_spent = models.IntegerField()
    
    redeemed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'reward_redemptions'
        verbose_name = 'Canje de Recompensa'
        verbose_name_plural = 'Canjes de Recompensas'
        ordering = ['-redeemed_at']
    
    def __str__(self):
        return f"{self.user.name} - {self.reward.name}"
