import uuid
from django.db import models
from django.conf import settings
from apps.jobs.models import Job


class Application(models.Model):
    """Job application model"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('interview', 'Interview'),
        ('offered', 'Offered'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    
    # Application details
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    portfolio_url = models.URLField(max_length=500, null=True, blank=True)
    
    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    status_notes = models.TextField(blank=True)
    
    # Timestamps
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Interview scheduling
    interview_scheduled_at = models.DateTimeField(null=True, blank=True)
    interview_location = models.CharField(max_length=500, blank=True)
    interview_notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-applied_at']
        unique_together = ['job', 'applicant']
        indexes = [
            models.Index(fields=['-applied_at']),
            models.Index(fields=['status', '-applied_at']),
        ]
    
    def __str__(self):
        return f"{self.applicant.name} applied to {self.job.title}"
    
    @property
    def is_active(self):
        """Check if application is still active (not rejected/withdrawn/accepted)"""
        return self.status in ['pending', 'reviewed', 'interview', 'offered']
