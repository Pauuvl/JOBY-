"""
User Model with Extended Profile
"""
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User model with additional fields for job seekers"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, verbose_name='Email Address')
    name = models.CharField(max_length=255, verbose_name='Full Name')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Phone Number')
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name='Profile Image')
    resume = models.FileField(upload_to='resumes/', blank=True, null=True, verbose_name='Resume/CV')
    
    # Professional Info
    age = models.IntegerField(blank=True, null=True, verbose_name='Age')
    experience = models.TextField(blank=True, null=True, verbose_name='Work Experience')
    education = models.TextField(blank=True, null=True, verbose_name='Education')
    location = models.CharField(max_length=255, blank=True, null=True, verbose_name='Location')
    skills = models.JSONField(default=list, blank=True, verbose_name='Skills')
    
    # Account Status
    is_active = models.BooleanField(default=True, verbose_name='Active')
    email_verified = models.BooleanField(default=False, verbose_name='Email Verified')
    
    # Points and Gamification
    points = models.IntegerField(default=0, verbose_name='Puntos Acumulados')
    
    # FCM Token for push notifications
    fcm_token = models.CharField(max_length=255, blank=True, null=True, verbose_name='FCM Token')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Override username field to use email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.email})"
    
    @property
    def profile_completion_percentage(self):
        """Calculate profile completion percentage"""
        fields = [
            self.name,
            self.email,
            self.phone,
            self.location,
            self.experience,
            self.education,
            self.skills,
            self.profile_image,
            self.resume,
        ]
        completed = sum(1 for field in fields if field)
        return int((completed / len(fields)) * 100)
    
    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name.split()[0] if self.name else self.username


class MotivationalMessage(models.Model):
    """Mensajes motivacionales para mostrar en la app"""
    
    CATEGORY_CHOICES = [
        ('motivation', 'Motivación'),
        ('job_search', 'Búsqueda de Empleo'),
        ('career', 'Desarrollo de Carrera'),
        ('perseverance', 'Perseverancia'),
        ('success', 'Éxito'),
        ('growth', 'Crecimiento'),
        ('positivity', 'Positividad'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.TextField(verbose_name='Mensaje')
    author = models.CharField(max_length=200, blank=True, null=True, verbose_name='Autor')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='motivation', verbose_name='Categoría')
    
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    priority = models.IntegerField(default=0, verbose_name='Prioridad', help_text='Mayor prioridad = más probabilidad de mostrarse')
    
    times_shown = models.IntegerField(default=0, verbose_name='Veces mostrado')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'motivational_messages'
        verbose_name = 'Mensaje Motivacional'
        verbose_name_plural = 'Mensajes Motivacionales'
        ordering = ['-priority', '-created_at']
    
    def __str__(self):
        return f"{self.message[:50]}..." if len(self.message) > 50 else self.message
    
    def increment_shown_count(self):
        """Incrementar el contador de veces mostrado"""
        self.times_shown += 1
        self.save(update_fields=['times_shown'])


class JobAlertPreference(models.Model):
    """Preferencias de alertas de trabajo del usuario"""
    
    FREQUENCY_CHOICES = [
        ('instant', 'Inmediata'),
        ('daily', 'Diaria'),
        ('weekly', 'Semanal'),
        ('disabled', 'Desactivada'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='job_alert_preference')
    
    # Configuración de alertas
    is_enabled = models.BooleanField(default=True, verbose_name='Alertas Activadas')
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='instant', verbose_name='Frecuencia')
    
    # Criterios de matching
    match_by_skills = models.BooleanField(default=True, verbose_name='Coincidir por Habilidades')
    match_by_location = models.BooleanField(default=True, verbose_name='Coincidir por Ubicación')
    match_by_experience = models.BooleanField(default=True, verbose_name='Coincidir por Experiencia')
    
    # Preferencias de trabajo
    preferred_job_types = models.JSONField(default=list, blank=True, verbose_name='Tipos de Trabajo Preferidos')
    preferred_locations = models.JSONField(default=list, blank=True, verbose_name='Ubicaciones Preferidas')
    remote_only = models.BooleanField(default=False, verbose_name='Solo Remoto')
    
    # Salario mínimo deseado
    min_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Salario Mínimo')
    
    # Última alerta enviada
    last_alert_sent = models.DateTimeField(null=True, blank=True, verbose_name='Última Alerta Enviada')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'job_alert_preferences'
        verbose_name = 'Preferencia de Alerta de Trabajo'
        verbose_name_plural = 'Preferencias de Alertas de Trabajo'
    
    def __str__(self):
        return f"Alertas de {self.user.name} - {'Activadas' if self.is_enabled else 'Desactivadas'}"


# Import course models
from .models_courses import Company, Course, UserCourse

# Import mentorship models
from .models_mentorship import SuccessStory, ProfileMatch, MentorshipRequest

__all__ = [
    'User', 'MotivationalMessage', 'JobAlertPreference',
    'Company', 'Course', 'UserCourse',
    'SuccessStory', 'ProfileMatch', 'MentorshipRequest'
]
