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
    experience = models.TextField(blank=True, null=True, verbose_name='Work Experience')
    education = models.TextField(blank=True, null=True, verbose_name='Education')
    location = models.CharField(max_length=255, blank=True, null=True, verbose_name='Location')
    skills = models.JSONField(default=list, blank=True, verbose_name='Skills')
    
    # Account Status
    is_active = models.BooleanField(default=True, verbose_name='Active')
    email_verified = models.BooleanField(default=False, verbose_name='Email Verified')
    
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
