"""
Models for mentorship matching system
"""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class SuccessStory(models.Model):
    """Track users who successfully got employed"""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='success_story'
    )
    
    # Employment details
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    hire_date = models.DateField()
    
    # Salary information (optional)
    SALARY_RANGES = [
        ('0-30k', '$0 - $30,000'),
        ('30k-50k', '$30,000 - $50,000'),
        ('50k-70k', '$50,000 - $70,000'),
        ('70k-100k', '$70,000 - $100,000'),
        ('100k+', '$100,000+'),
    ]
    salary_range = models.CharField(
        max_length=20,
        choices=SALARY_RANGES,
        blank=True,
        null=True
    )
    
    # Mentorship availability
    is_willing_to_mentor = models.BooleanField(default=False)
    max_mentees = models.IntegerField(default=3)
    
    # Story details
    success_description = models.TextField(
        help_text="¿Cómo conseguiste el empleo? Consejos para otros"
    )
    key_skills_used = models.JSONField(
        default=list,
        help_text="Skills que fueron clave para conseguir el empleo"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'success_stories'
        ordering = ['-hire_date']
        verbose_name = 'Historia de Éxito'
        verbose_name_plural = 'Historias de Éxito'
    
    def __str__(self):
        return f"{self.user.name} - {self.position} at {self.company}"
    
    @property
    def current_mentees_count(self):
        """Count active mentees"""
        return self.user.mentorship_requests_received.filter(
            status='accepted'
        ).count()
    
    @property
    def can_accept_mentees(self):
        """Check if can accept more mentees"""
        return (
            self.is_willing_to_mentor and 
            self.is_active and
            self.current_mentees_count < self.max_mentees
        )


class ProfileMatch(models.Model):
    """Store calculated profile similarity scores"""
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='profile_matches'
    )
    matched_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='matched_by'
    )
    
    similarity_score = models.IntegerField(
        help_text="Similarity score 0-100"
    )
    
    # Matching factors
    matching_skills = models.JSONField(
        default=list,
        help_text="Skills in common"
    )
    skill_overlap_percentage = models.FloatField(default=0.0)
    
    # Additional matching factors
    same_location = models.BooleanField(default=False)
    similar_experience_level = models.BooleanField(default=False)
    
    # Metadata
    calculated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'profile_matches'
        ordering = ['-similarity_score']
        unique_together = ['user', 'matched_user']
        indexes = [
            models.Index(fields=['user', '-similarity_score']),
            models.Index(fields=['matched_user', '-similarity_score']),
        ]
    
    def __str__(self):
        return f"{self.user.name} <-> {self.matched_user.name} ({self.similarity_score}%)"


class MentorshipRequest(models.Model):
    """Track mentorship connection requests"""
    
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('accepted', 'Aceptada'),
        ('declined', 'Rechazada'),
        ('cancelled', 'Cancelada'),
    ]
    
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='mentorship_requests_sent'
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='mentorship_requests_received'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    message = models.TextField(
        help_text="Mensaje de presentación"
    )
    
    # Response
    response_message = models.TextField(blank=True, null=True)
    responded_at = models.DateTimeField(blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'mentorship_requests'
        ordering = ['-created_at']
        unique_together = ['from_user', 'to_user']
        indexes = [
            models.Index(fields=['from_user', '-created_at']),
            models.Index(fields=['to_user', 'status', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.from_user.name} -> {self.to_user.name} ({self.status})"
    
    @property
    def status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)


__all__ = [
    'SuccessStory',
    'ProfileMatch',
    'MentorshipRequest',
]
