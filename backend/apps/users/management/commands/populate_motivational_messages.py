"""
Management command para poblar la base de datos con mensajes motivacionales
"""
from django.core.management.base import BaseCommand
from apps.users.models import MotivationalMessage


class Command(BaseCommand):
    help = 'Poblar la base de datos con mensajes motivacionales'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creando mensajes motivacionales...'))
        
        messages = [
            # Motivación General
            {
                'message': '¡Cada día es una nueva oportunidad para acercarte a tus metas! 🌟',
                'author': 'Joby Team',
                'category': 'motivation',
                'priority': 10
            },
            {
                'message': 'El éxito es la suma de pequeños esfuerzos repetidos día tras día.',
                'author': 'Robert Collier',
                'category': 'motivation',
                'priority': 8
            },
            {
                'message': '¡No te rindas! Cada aplicación te acerca más a tu trabajo ideal.',
                'author': None,
                'category': 'motivation',
                'priority': 9
            },
            {
                'message': 'Tu actitud determina tu dirección. ¡Mantén la mente positiva! 💪',
                'author': None,
                'category': 'positivity',
                'priority': 7
            },
            
            # Búsqueda de Empleo
            {
                'message': 'La persistencia es clave en la búsqueda de empleo. ¡Sigue adelante! 🎯',
                'author': None,
                'category': 'job_search',
                'priority': 10
            },
            {
                'message': 'Cada "no" te acerca más a un "sí". ¡No dejes de aplicar!',
                'author': None,
                'category': 'job_search',
                'priority': 9
            },
            {
                'message': 'Prepara tu CV hoy, podrías recibir una oportunidad mañana. 📄',
                'author': None,
                'category': 'job_search',
                'priority': 8
            },
            {
                'message': 'Las mejores oportunidades vienen cuando menos las esperas. ¡Mantente preparado!',
                'author': None,
                'category': 'job_search',
                'priority': 7
            },
            
            # Desarrollo de Carrera
            {
                'message': 'Invierte en ti mismo. El aprendizaje continuo es la clave del éxito. 📚',
                'author': None,
                'category': 'career',
                'priority': 8
            },
            {
                'message': 'Tu próxima habilidad podría ser la puerta a tu próximo trabajo. 🚪',
                'author': None,
                'category': 'career',
                'priority': 7
            },
            {
                'message': 'El networking es tan importante como las habilidades técnicas. ¡Conéctate!',
                'author': None,
                'category': 'career',
                'priority': 6
            },
            
            # Perseverancia
            {
                'message': 'La diferencia entre ganar y perder es nunca rendirse.',
                'author': 'Walt Disney',
                'category': 'perseverance',
                'priority': 9
            },
            {
                'message': '¡Los obstáculos son oportunidades disfrazadas! 💎',
                'author': None,
                'category': 'perseverance',
                'priority': 8
            },
            {
                'message': 'El fracaso es solo una oportunidad para comenzar de nuevo con más inteligencia.',
                'author': 'Henry Ford',
                'category': 'perseverance',
                'priority': 7
            },
            
            # Éxito
            {
                'message': 'El éxito no es un destino, es un viaje. Disfruta cada paso. 🛤️',
                'author': None,
                'category': 'success',
                'priority': 8
            },
            {
                'message': 'Tu trabajo va a llenar gran parte de tu vida. Asegúrate de que sea algo que te apasione.',
                'author': 'Steve Jobs',
                'category': 'success',
                'priority': 9
            },
            {
                'message': 'El único límite para tus logros es el que tú mismo te impongas.',
                'author': None,
                'category': 'success',
                'priority': 7
            },
            
            # Crecimiento Personal
            {
                'message': 'Cada error es una lección. Cada lección es crecimiento. 🌱',
                'author': None,
                'category': 'growth',
                'priority': 8
            },
            {
                'message': 'Sal de tu zona de confort. Ahí es donde sucede la magia. ✨',
                'author': None,
                'category': 'growth',
                'priority': 7
            },
            {
                'message': 'La mejor versión de ti mismo está a solo un paso de distancia. ¡Da ese paso!',
                'author': None,
                'category': 'growth',
                'priority': 6
            },
            
            # Positividad
            {
                'message': 'Sonríe más, preocúpate menos. ¡Todo saldrá bien! 😊',
                'author': None,
                'category': 'positivity',
                'priority': 7
            },
            {
                'message': 'La actitud positiva es contagiosa. Compártela en cada entrevista. ✨',
                'author': None,
                'category': 'positivity',
                'priority': 8
            },
            {
                'message': 'Hoy es un gran día para conseguir ese trabajo que deseas. 🎉',
                'author': None,
                'category': 'positivity',
                'priority': 9
            },
            
            # Adicionales
            {
                'message': '¡Mantén tu racha! La consistencia es el camino al éxito. 🔥',
                'author': None,
                'category': 'motivation',
                'priority': 10
            },
            {
                'message': 'Cada entrevista es una oportunidad de aprender y mejorar. 🎯',
                'author': None,
                'category': 'job_search',
                'priority': 8
            },
            {
                'message': 'Tu próximo gran logro comienza con una simple acción hoy. 🚀',
                'author': None,
                'category': 'motivation',
                'priority': 9
            },
        ]
        
        created_count = 0
        for msg_data in messages:
            message, created = MotivationalMessage.objects.get_or_create(
                message=msg_data['message'],
                defaults={
                    'author': msg_data['author'],
                    'category': msg_data['category'],
                    'priority': msg_data['priority'],
                    'is_active': True
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Creado: {msg_data["message"][:50]}...'))
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Se crearon {created_count} mensajes nuevos.'))
        self.stdout.write(self.style.SUCCESS(f'✓ Total de mensajes en la base de datos: {MotivationalMessage.objects.count()}'))
