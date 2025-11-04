import uuid
from django.db import models
from django.conf import settings


class Job(models.Model):
    """Job posting model"""
    
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('freelance', 'Freelance'),
    ]
    
    EXPERIENCE_LEVEL_CHOICES = [
        ('entry', 'Entry Level'),
        ('mid', 'Mid Level'),
        ('senior', 'Senior Level'),
        ('lead', 'Lead'),
        ('executive', 'Executive'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    company_logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    location = models.CharField(max_length=200)
    remote_ok = models.BooleanField(default=False)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL_CHOICES)
    
    description = models.TextField()
    requirements = models.JSONField(default=list)  # List of requirement strings
    responsibilities = models.JSONField(default=list)  # List of responsibility strings
    benefits = models.JSONField(default=list)  # List of benefit strings
    skills_required = models.JSONField(default=list)  # List of skill strings
    
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_currency = models.CharField(max_length=3, default='USD')
    
    application_url = models.URLField(max_length=500, null=True, blank=True)
    application_email = models.EmailField(null=True, blank=True)
    
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posted_jobs')
    posted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    views_count = models.IntegerField(default=0)
    
    # SEO fields
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    
    class Meta:
        ordering = ['-posted_at']
        indexes = [
            models.Index(fields=['-posted_at']),
            models.Index(fields=['is_active', '-posted_at']),
            models.Index(fields=['job_type', '-posted_at']),
        ]
    
    def __str__(self):
        return f"{self.title} at {self.company_name}"
    
    def save(self, *args, **kwargs):
        # Generate slug from title and company if not set
        if not self.slug:
            from django.utils.text import slugify
            base_slug = slugify(f"{self.title}-{self.company_name}")
            self.slug = f"{base_slug}-{str(self.id)[:8]}"
        super().save(*args, **kwargs)
    
    @property
    def salary_range(self):
        """Returns formatted salary range"""
        if self.salary_min and self.salary_max:
            return f"{self.salary_currency} {self.salary_min:,.0f} - {self.salary_max:,.0f}"
        elif self.salary_min:
            return f"From {self.salary_currency} {self.salary_min:,.0f}"
        return "Competitive"
    
    @property
    def is_expired(self):
        """Check if job posting has expired"""
        if self.expires_at:
            from django.utils import timezone
            return timezone.now() > self.expires_at
        return False


class SavedJob(models.Model):
    """Track jobs saved by users"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'job']
        ordering = ['-saved_at']
    
    def __str__(self):
        return f"{self.user.name} saved {self.job.title}"
