"""
Comando para enviar alertas de trabajo de prueba
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.users.models import User, JobAlertPreference
from apps.jobs.models import Job
from apps.jobs.services import JobMatchingService
from apps.notifications.models import Notification


class Command(BaseCommand):
    help = 'Envía alertas de trabajo de prueba a todos los usuarios o a un usuario específico'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email del usuario específico',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Enviar a todos los usuarios',
        )
        parser.add_argument(
            '--create-jobs',
            action='store_true',
            help='Crear trabajos de prueba antes de enviar alertas',
        )

    def handle(self, *args, **options):
        email = options.get('email')
        send_all = options.get('all')
        create_jobs = options.get('create_jobs')

        # Crear trabajos de prueba si se solicita
        if create_jobs:
            self.stdout.write(self.style.SUCCESS('📝 Creando trabajos de prueba...'))
            self._create_sample_jobs()

        # Determinar usuarios a procesar
        if email:
            try:
                user = User.objects.get(email=email)
                users = [user]
                self.stdout.write(self.style.SUCCESS(f'👤 Usuario encontrado: {user.name} ({user.email})'))
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'❌ Usuario con email {email} no encontrado'))
                return
        elif send_all:
            users = User.objects.filter(is_active=True)
            self.stdout.write(self.style.SUCCESS(f'👥 Procesando {users.count()} usuarios activos...'))
        else:
            self.stdout.write(self.style.ERROR('❌ Debes especificar --email <email> o --all'))
            return

        # Procesar cada usuario
        alerts_sent = 0
        for user in users:
            try:
                # Asegurar que el usuario tenga preferencias
                preference, created = JobAlertPreference.objects.get_or_create(
                    user=user,
                    defaults={'is_enabled': True, 'frequency': 'instant'}
                )
                
                if created:
                    self.stdout.write(f'  ✨ Preferencias creadas para {user.email}')
                
                # Habilitar alertas temporalmente si están deshabilitadas
                was_disabled = not preference.is_enabled
                if was_disabled:
                    preference.is_enabled = True
                    preference.save()

                # Buscar trabajos coincidentes
                matching_jobs = JobMatchingService.find_matching_jobs(user, min_score=50, limit=5)
                
                if matching_jobs:
                    # Enviar alerta
                    notification = JobMatchingService.send_job_alert(user, matching_jobs)
                    
                    if notification:
                        alerts_sent += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'  ✅ Alerta enviada a {user.email}: '
                                f'{len(matching_jobs)} trabajos encontrados '
                                f'(mejor match: {matching_jobs[0]["score"]}%)'
                            )
                        )
                        
                        # Mostrar detalles de los trabajos
                        for i, job_data in enumerate(matching_jobs[:3], 1):
                            job = job_data['job']
                            self.stdout.write(
                                f'     {i}. {job.title} en {job.company_name} '
                                f'- Match: {job_data["score"]}%'
                            )
                    else:
                        self.stdout.write(self.style.WARNING(f'  ⚠️  No se pudo crear alerta para {user.email}'))
                else:
                    self.stdout.write(self.style.WARNING(f'  ⚠️  No hay trabajos coincidentes para {user.email}'))
                
                # Restaurar estado original si estaba deshabilitado
                if was_disabled:
                    preference.is_enabled = False
                    preference.save()
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ❌ Error procesando {user.email}: {str(e)}'))

        # Resumen
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS(f'🎉 Proceso completado: {alerts_sent} alertas enviadas de {len(users)} usuarios'))
        self.stdout.write(self.style.SUCCESS('='*60))
        
        # Mostrar cómo ver las notificaciones
        self.stdout.write('')
        self.stdout.write(self.style.WARNING('📱 Para ver las notificaciones en Flutter:'))
        self.stdout.write('   1. Abre la app en Flutter')
        self.stdout.write('   2. Ve a la pantalla de notificaciones (ícono de campana)')
        self.stdout.write('   3. O verifica en: GET /api/notifications/')

    def _create_sample_jobs(self):
        """Crear trabajos de prueba con diferentes características"""
        
        # Obtener un usuario admin para posted_by
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.first()
        
        if not admin_user:
            self.stdout.write(self.style.ERROR('❌ No hay usuarios en la base de datos'))
            return

        sample_jobs = [
            {
                'title': 'Desarrollador Python Senior',
                'company_name': 'TechCorp',
                'location': 'Ciudad de México, México',
                'remote_ok': True,
                'job_type': 'full_time',
                'experience_level': 'senior',
                'description': 'Buscamos un desarrollador Python experimentado para unirse a nuestro equipo.',
                'skills_required': ['Python', 'Django', 'PostgreSQL', 'Docker', 'AWS'],
                'salary_min': 80000,
                'salary_max': 120000,
                'is_active': True,
            },
            {
                'title': 'Frontend Developer React',
                'company_name': 'Startup Innovadora',
                'location': 'Guadalajara, México',
                'remote_ok': True,
                'job_type': 'full_time',
                'experience_level': 'mid',
                'description': 'Únete a nuestro equipo para crear interfaces increíbles.',
                'skills_required': ['React', 'JavaScript', 'TypeScript', 'CSS', 'Git'],
                'salary_min': 50000,
                'salary_max': 75000,
                'is_active': True,
            },
            {
                'title': 'Full Stack Developer',
                'company_name': 'Digital Agency',
                'location': 'Remoto, México',
                'remote_ok': True,
                'job_type': 'full_time',
                'experience_level': 'mid',
                'description': 'Desarrollador full stack para proyectos diversos.',
                'skills_required': ['JavaScript', 'Node.js', 'React', 'MongoDB', 'Express'],
                'salary_min': 60000,
                'salary_max': 90000,
                'is_active': True,
            },
            {
                'title': 'Data Scientist',
                'company_name': 'Analytics Co',
                'location': 'Monterrey, México',
                'remote_ok': False,
                'job_type': 'full_time',
                'experience_level': 'senior',
                'description': 'Científico de datos para análisis avanzados.',
                'skills_required': ['Python', 'Machine Learning', 'TensorFlow', 'Pandas', 'SQL'],
                'salary_min': 90000,
                'salary_max': 130000,
                'is_active': True,
            },
            {
                'title': 'Mobile Developer Flutter',
                'company_name': 'App Masters',
                'location': 'Remoto, LATAM',
                'remote_ok': True,
                'job_type': 'contract',
                'experience_level': 'mid',
                'description': 'Desarrollador Flutter para aplicaciones móviles.',
                'skills_required': ['Flutter', 'Dart', 'Firebase', 'Git', 'REST APIs'],
                'salary_min': 55000,
                'salary_max': 85000,
                'is_active': True,
            },
        ]

        created_count = 0
        for job_data in sample_jobs:
            job_data['posted_by'] = admin_user
            job_data['posted_at'] = timezone.now()
            
            # Verificar si ya existe un trabajo similar
            existing = Job.objects.filter(
                title=job_data['title'],
                company_name=job_data['company_name']
            ).first()
            
            if not existing:
                Job.objects.create(**job_data)
                created_count += 1
                self.stdout.write(f'  ✅ Creado: {job_data["title"]} en {job_data["company_name"]}')

        self.stdout.write(self.style.SUCCESS(f'📝 {created_count} trabajos de prueba creados\n'))
