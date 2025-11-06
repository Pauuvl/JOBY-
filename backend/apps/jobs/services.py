"""
Job Matching and Alert Services
"""
from django.db.models import Q
from django.utils import timezone
from .models import Job
from apps.notifications.models import Notification


class JobMatchingService:
    """Servicio para matching de trabajos con perfiles de usuarios"""
    
    @staticmethod
    def calculate_match_score(job, user):
        """
        Calcula un score de coincidencia entre un trabajo y un usuario (0-100)
        """
        score = 0
        max_score = 0
        
        # 1. Matching por habilidades (peso: 40%)
        max_score += 40
        if user.skills and job.skills_required:
            user_skills_lower = [skill.lower() for skill in user.skills]
            job_skills_lower = [skill.lower() for skill in job.skills_required]
            
            matching_skills = set(user_skills_lower) & set(job_skills_lower)
            if job_skills_lower:
                skill_match_percentage = len(matching_skills) / len(job_skills_lower)
                score += skill_match_percentage * 40
        
        # 2. Matching por ubicación (peso: 30%)
        max_score += 30
        if user.location and job.location:
            # Si el trabajo es remoto, coincide con cualquier ubicación
            if job.remote_ok:
                score += 30
            # Si las ubicaciones coinciden parcialmente
            elif user.location.lower() in job.location.lower() or job.location.lower() in user.location.lower():
                score += 30
            # Si ambas están en el mismo país (comparación básica)
            elif user.location.split(',')[-1].strip().lower() == job.location.split(',')[-1].strip().lower():
                score += 15
        elif job.remote_ok:
            score += 30
        
        # 3. Matching por nivel de experiencia (peso: 30%)
        max_score += 30
        if user.experience:
            # Análisis simple del texto de experiencia
            experience_text = user.experience.lower()
            
            experience_level_map = {
                'entry': ['junior', 'entry', 'beginner', 'recién graduado', 'sin experiencia'],
                'mid': ['mid', 'intermedio', 'intermediate', '2 años', '3 años', '4 años'],
                'senior': ['senior', 'sénior', 'avanzado', 'experto', '5 años', '6 años', '7 años'],
                'lead': ['lead', 'líder', 'jefe', 'gerente', 'manager'],
                'executive': ['executive', 'director', 'ejecutivo', 'c-level', 'vp', 'ceo', 'cto'],
            }
            
            # Determinar nivel del usuario basado en palabras clave
            user_level = None
            for level, keywords in experience_level_map.items():
                if any(keyword in experience_text for keyword in keywords):
                    user_level = level
                    break
            
            # Si coincide el nivel exacto
            if user_level == job.experience_level:
                score += 30
            # Si el usuario tiene un nivel superior (puede aplicar a junior siendo senior)
            elif user_level and experience_level_map.keys():
                levels_order = ['entry', 'mid', 'senior', 'lead', 'executive']
                if user_level in levels_order and job.experience_level in levels_order:
                    user_index = levels_order.index(user_level)
                    job_index = levels_order.index(job.experience_level)
                    if user_index > job_index:
                        score += 15  # Penalizar overqualification
                    elif user_index == job_index - 1:
                        score += 25  # Un nivel debajo está bien
        
        return min(round(score), 100)
    
    @staticmethod
    def find_matching_jobs(user, min_score=60, limit=10):
        """
        Encuentra trabajos que coincidan con el perfil del usuario
        """
        from apps.users.models import JobAlertPreference
        
        # Obtener preferencias del usuario
        try:
            preferences = user.job_alert_preference
        except JobAlertPreference.DoesNotExist:
            # Crear preferencias por defecto
            preferences = JobAlertPreference.objects.create(user=user)
        
        # Si las alertas están desactivadas, retornar lista vacía
        if not preferences.is_enabled:
            return []
        
        # Filtros base
        jobs_query = Job.objects.filter(is_active=True)
        
        # Aplicar filtros de preferencias
        if preferences.remote_only:
            jobs_query = jobs_query.filter(remote_ok=True)
        
        if preferences.preferred_job_types:
            jobs_query = jobs_query.filter(job_type__in=preferences.preferred_job_types)
        
        if preferences.preferred_locations:
            location_q = Q()
            for location in preferences.preferred_locations:
                location_q |= Q(location__icontains=location)
            jobs_query = jobs_query.filter(location_q | Q(remote_ok=True))
        
        if preferences.min_salary:
            jobs_query = jobs_query.filter(
                Q(salary_min__gte=preferences.min_salary) | 
                Q(salary_max__gte=preferences.min_salary) |
                Q(salary_min__isnull=True, salary_max__isnull=True)
            )
        
        # Calcular score para cada trabajo
        matching_jobs = []
        for job in jobs_query[:50]:  # Limitar a 50 para no sobrecargar
            score = JobMatchingService.calculate_match_score(job, user)
            if score >= min_score:
                matching_jobs.append({
                    'job': job,
                    'score': score,
                    'matching_skills': JobMatchingService._get_matching_skills(job, user)
                })
        
        # Ordenar por score y limitar
        matching_jobs.sort(key=lambda x: x['score'], reverse=True)
        return matching_jobs[:limit]
    
    @staticmethod
    def _get_matching_skills(job, user):
        """Retorna las habilidades que coinciden entre el trabajo y el usuario"""
        if not user.skills or not job.skills_required:
            return []
        
        user_skills_lower = [skill.lower() for skill in user.skills]
        job_skills_lower = [skill.lower() for skill in job.skills_required]
        
        matching = []
        for skill in job.skills_required:
            if skill.lower() in user_skills_lower:
                matching.append(skill)
        
        return matching
    
    @staticmethod
    def send_job_alert(user, jobs_data):
        """
        Envía una notificación al usuario sobre nuevos trabajos relevantes
        """
        if not jobs_data:
            return None
        
        # Crear notificación en la app
        top_job = jobs_data[0]['job']
        
        if len(jobs_data) == 1:
            title = "¡Nueva vacante perfecta para ti!"
            message = f"{top_job.title} en {top_job.company_name} - {jobs_data[0]['score']}% match"
        else:
            title = f"¡{len(jobs_data)} nuevas vacantes para ti!"
            message = f"Incluyendo {top_job.title} en {top_job.company_name}"
        
        notification = Notification.objects.create(
            recipient=user,
            notification_type='new_job',
            title=title,
            message=message,
            data={
                'jobs': [
                    {
                        'id': str(job_data['job'].id),
                        'title': job_data['job'].title,
                        'company': job_data['job'].company_name,
                        'score': job_data['score'],
                        'matching_skills': job_data['matching_skills']
                    }
                    for job_data in jobs_data[:5]  # Máximo 5 trabajos en la notificación
                ]
            },
            action_url=f"/jobs/{top_job.id}"
        )
        
        # Actualizar última alerta enviada
        from apps.users.models import JobAlertPreference
        try:
            preferences = user.job_alert_preference
            preferences.last_alert_sent = timezone.now()
            preferences.save(update_fields=['last_alert_sent'])
        except JobAlertPreference.DoesNotExist:
            pass
        
        return notification
    
    @staticmethod
    def check_new_jobs_for_user(user):
        """
        Verifica si hay nuevos trabajos para un usuario y envía alertas si corresponde
        """
        from apps.users.models import JobAlertPreference
        
        try:
            preferences = user.job_alert_preference
        except JobAlertPreference.DoesNotExist:
            return None
        
        # Verificar si debe enviar alertas según frecuencia
        now = timezone.now()
        should_send = False
        
        if preferences.frequency == 'disabled' or not preferences.is_enabled:
            return None
        
        if preferences.frequency == 'instant':
            should_send = True
        elif preferences.frequency == 'daily' and (
            not preferences.last_alert_sent or 
            (now - preferences.last_alert_sent).days >= 1
        ):
            should_send = True
        elif preferences.frequency == 'weekly' and (
            not preferences.last_alert_sent or 
            (now - preferences.last_alert_sent).days >= 7
        ):
            should_send = True
        
        if not should_send:
            return None
        
        # Buscar trabajos nuevos desde la última alerta
        time_threshold = preferences.last_alert_sent or (now - timezone.timedelta(days=7))
        recent_jobs = Job.objects.filter(
            is_active=True,
            posted_at__gte=time_threshold
        )
        
        if not recent_jobs.exists():
            return None
        
        # Encontrar matches
        matching_jobs = JobMatchingService.find_matching_jobs(user, min_score=70)
        
        # Filtrar solo trabajos recientes
        recent_job_ids = set(str(job.id) for job in recent_jobs)
        recent_matches = [
            job_data for job_data in matching_jobs 
            if str(job_data['job'].id) in recent_job_ids
        ]
        
        if recent_matches:
            return JobMatchingService.send_job_alert(user, recent_matches)
        
        return None
