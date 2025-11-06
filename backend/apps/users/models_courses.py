import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone


class Company(models.Model):
    """Empresas que ofrecen cursos"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, verbose_name='Nombre')
    logo_url = models.URLField(blank=True, null=True, verbose_name='URL del logo')
    website = models.URLField(blank=True, null=True, verbose_name='Sitio web')
    description = models.TextField(blank=True, verbose_name='Descripción')
    is_active = models.BooleanField(default=True, verbose_name='Activa')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'companies'
        ordering = ['name']
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
    
    def __str__(self):
        return self.name


class Course(models.Model):
    """Cursos recomendados por empresas"""
    
    LEVEL_CHOICES = [
        ('beginner', 'Principiante'),
        ('intermediate', 'Intermedio'),
        ('advanced', 'Avanzado'),
        ('expert', 'Experto'),
    ]
    
    DURATION_UNIT_CHOICES = [
        ('hours', 'Horas'),
        ('days', 'Días'),
        ('weeks', 'Semanas'),
        ('months', 'Meses'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    title = models.CharField(max_length=200, verbose_name='Título')
    description = models.TextField(verbose_name='Descripción')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='courses', verbose_name='Empresa')
    
    # Skills related
    required_skills = models.JSONField(default=list, verbose_name='Habilidades requeridas',
                                      help_text='Lista de skills necesarias para el curso')
    skills_taught = models.JSONField(default=list, verbose_name='Habilidades enseñadas',
                                    help_text='Lista de skills que se aprenden en el curso')
    
    # Course details
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner', verbose_name='Nivel')
    duration_value = models.IntegerField(verbose_name='Duración (valor)')
    duration_unit = models.CharField(max_length=20, choices=DURATION_UNIT_CHOICES, verbose_name='Duración (unidad)')
    
    # Links
    course_url = models.URLField(verbose_name='URL del curso')
    thumbnail_url = models.URLField(blank=True, null=True, verbose_name='URL de miniatura')
    
    # Metadata
    is_free = models.BooleanField(default=False, verbose_name='Gratis')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Precio')
    currency = models.CharField(max_length=3, default='USD', verbose_name='Moneda')
    
    # Popularity
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name='Calificación')
    enrollments = models.IntegerField(default=0, verbose_name='Inscripciones')
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    priority = models.IntegerField(default=0, verbose_name='Prioridad')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'courses'
        ordering = ['-priority', '-rating', '-enrollments']
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        indexes = [
            models.Index(fields=['company', 'is_active']),
            models.Index(fields=['-priority', '-rating']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.company.name}"
    
    @property
    def duration_display(self):
        """Get human readable duration"""
        unit_map = {
            'hours': 'hora' if self.duration_value == 1 else 'horas',
            'days': 'día' if self.duration_value == 1 else 'días',
            'weeks': 'semana' if self.duration_value == 1 else 'semanas',
            'months': 'mes' if self.duration_value == 1 else 'meses',
        }
        return f"{self.duration_value} {unit_map.get(self.duration_unit, self.duration_unit)}"
    
    def calculate_match_score(self, user_skills):
        """Calculate how well this course matches user skills"""
        if not user_skills:
            return 0
        
        user_skills_set = set([skill.lower() for skill in user_skills])
        taught_skills_set = set([skill.lower() for skill in self.skills_taught])
        required_skills_set = set([skill.lower() for skill in self.required_skills])
        
        # Skills that user will learn (taught skills they don't have)
        new_skills = taught_skills_set - user_skills_set
        new_skills_score = len(new_skills) * 40  # 40% weight for new skills
        
        # Skills user already has that are required
        matching_required = user_skills_set.intersection(required_skills_set)
        prereq_score = (len(matching_required) / max(len(required_skills_set), 1)) * 30  # 30% weight
        
        # Level appropriateness
        level_score = 15 if self.level in ['beginner', 'intermediate'] else 10
        
        # Popularity bonus - Convert Decimal to float
        popularity_score = min(15, (float(self.rating) / 5.0) * 15)
        
        total_score = min(100, new_skills_score + prereq_score + level_score + popularity_score)
        
        return round(total_score)


class UserCourse(models.Model):
    """Track user enrollment in courses"""
    
    STATUS_CHOICES = [
        ('enrolled', 'Inscrito'),
        ('in_progress', 'En progreso'),
        ('completed', 'Completado'),
        ('abandoned', 'Abandonado'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrolled_courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments_detail')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enrolled', verbose_name='Estado')
    progress_percentage = models.IntegerField(default=0, verbose_name='Progreso (%)')
    
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_courses'
        unique_together = ['user', 'course']
        ordering = ['-enrolled_at']
        verbose_name = 'Curso de Usuario'
        verbose_name_plural = 'Cursos de Usuarios'
    
    def __str__(self):
        return f"{self.user.name} - {self.course.title} ({self.status})"
