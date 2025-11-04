from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.streaks.models import Challenge


class Command(BaseCommand):
    help = 'Popula la base de datos con retos de ejemplo'

    def handle(self, *args, **options):
        challenges_data = [
            # Daily Challenges - Job Applications
            {
                'title': '¡Postúlate hoy!',
                'description': 'Envía tu solicitud a 3 empleos diferentes hoy',
                'challenge_type': 'daily',
                'category': 'applications',
                'target_count': 3,
                'points_reward': 50,
                'icon': '📧',
            },
            {
                'title': 'Explorador de oportunidades',
                'description': 'Visualiza y guarda 10 ofertas de trabajo que te interesen',
                'challenge_type': 'daily',
                'category': 'job_search',
                'target_count': 10,
                'points_reward': 30,
                'icon': '🔍',
            },
            {
                'title': 'Perfil al día',
                'description': 'Actualiza tu perfil profesional hoy',
                'challenge_type': 'daily',
                'category': 'profile',
                'target_count': 1,
                'points_reward': 40,
                'icon': '👤',
            },
            {
                'title': 'Quick Apply',
                'description': 'Postúlate a un empleo en menos de 5 minutos',
                'challenge_type': 'daily',
                'category': 'applications',
                'target_count': 1,
                'points_reward': 25,
                'icon': '⚡',
            },
            {
                'title': 'Persistencia diaria',
                'description': 'Mantén tu racha del día completando tu reto diario',
                'challenge_type': 'daily',
                'category': 'streak',
                'target_count': 1,
                'points_reward': 20,
                'icon': '🔥',
            },
            
            # Weekly Challenges - More ambitious goals
            {
                'title': 'Semana productiva',
                'description': 'Postúlate a 10 empleos diferentes durante esta semana',
                'challenge_type': 'weekly',
                'category': 'applications',
                'target_count': 10,
                'points_reward': 200,
                'icon': '🎯',
            },
            {
                'title': 'Explorador semanal',
                'description': 'Revisa al menos 50 ofertas de empleo esta semana',
                'challenge_type': 'weekly',
                'category': 'job_search',
                'target_count': 50,
                'points_reward': 150,
                'icon': '🗺️',
            },
            {
                'title': 'Racha de 7 días',
                'description': 'Mantén una racha activa durante 7 días consecutivos',
                'challenge_type': 'weekly',
                'category': 'streak',
                'target_count': 7,
                'points_reward': 250,
                'icon': '🔥',
            },
            {
                'title': 'Mejora continua',
                'description': 'Actualiza tu perfil 3 veces esta semana',
                'challenge_type': 'weekly',
                'category': 'profile',
                'target_count': 3,
                'points_reward': 120,
                'icon': '📈',
            },
            {
                'title': 'Super aplicador',
                'description': 'Envía 20 solicitudes de empleo esta semana',
                'challenge_type': 'weekly',
                'category': 'applications',
                'target_count': 20,
                'points_reward': 300,
                'icon': '🚀',
            },
            
            # Special Challenges - Limited time or special events
            {
                'title': 'Primera postulación',
                'description': 'Completa tu primera solicitud de empleo en JOBY',
                'challenge_type': 'special',
                'category': 'milestone',
                'target_count': 1,
                'points_reward': 100,
                'icon': '🎉',
            },
            {
                'title': 'Perfil completo',
                'description': 'Completa el 100% de tu perfil profesional',
                'challenge_type': 'special',
                'category': 'profile',
                'target_count': 1,
                'points_reward': 150,
                'icon': '✅',
            },
            {
                'title': 'Maratón de aplicaciones',
                'description': 'Postúlate a 5 empleos en un solo día',
                'challenge_type': 'special',
                'category': 'applications',
                'target_count': 5,
                'points_reward': 100,
                'icon': '🏃',
            },
            {
                'title': 'Campeón mensual',
                'description': 'Postúlate a 50 empleos en un mes',
                'challenge_type': 'special',
                'category': 'applications',
                'target_count': 50,
                'points_reward': 500,
                'icon': '👑',
            },
            {
                'title': 'Racha legendaria',
                'description': 'Alcanza una racha de 30 días consecutivos',
                'challenge_type': 'special',
                'category': 'streak',
                'target_count': 30,
                'points_reward': 1000,
                'icon': '⭐',
            },
        ]

        created_count = 0
        updated_count = 0

        for challenge_data in challenges_data:
            challenge, created = Challenge.objects.update_or_create(
                title=challenge_data['title'],
                defaults=challenge_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Creado: {challenge.title}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'↻ Actualizado: {challenge.title}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n¡Listo! {created_count} retos creados, {updated_count} actualizados.'
            )
        )
