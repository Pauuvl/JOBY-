"""
Management command para probar el envío de recordatorios de racha
"""
from django.core.management.base import BaseCommand
from apps.notifications.tasks import send_streak_reminders


class Command(BaseCommand):
    help = 'Envía recordatorios de racha a usuarios que no han completado el reto del día'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando envío de recordatorios de racha...'))
        
        result = send_streak_reminders()
        
        self.stdout.write(self.style.SUCCESS(f'✓ {result}'))
