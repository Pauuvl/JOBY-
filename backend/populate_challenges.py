"""
Script to populate challenges for streaks system
Run: python populate_challenges.py
"""
import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'joby_api.settings')
django.setup()

from apps.streaks.models import Challenge, UserChallenge
from django.contrib.auth import get_user_model

User = get_user_model()


def create_challenges():
    """Create various challenges"""
    
    challenges_data = [
        # DAILY CHALLENGES
        {
            'title': 'Primera Aplicación del Día',
            'description': 'Aplica a tu primer trabajo del día y comienza con energía',
            'icon': '🌅',
            'challenge_type': 'daily',
            'category': 'applications',
            'target_action': 'apply_to_jobs',
            'target_count': 1,
            'points_reward': 10,
            'priority': 100
        },
        {
            'title': 'Aplicador Activo',
            'description': 'Aplica a 5 trabajos en un solo día',
            'icon': '🎯',
            'challenge_type': 'daily',
            'category': 'applications',
            'target_action': 'apply_to_jobs',
            'target_count': 5,
            'points_reward': 50,
            'priority': 90
        },
        {
            'title': 'Actualiza tu Perfil',
            'description': 'Mejora tu información de perfil para destacar',
            'icon': '✏️',
            'challenge_type': 'daily',
            'category': 'profile',
            'target_action': 'update_profile',
            'target_count': 1,
            'points_reward': 20,
            'priority': 85
        },
        {
            'title': 'Explorador de Oportunidades',
            'description': 'Revisa al menos 10 ofertas de trabajo',
            'icon': '🔍',
            'challenge_type': 'daily',
            'category': 'exploration',
            'target_action': 'view_jobs',
            'target_count': 10,
            'points_reward': 15,
            'priority': 80
        },
        {
            'title': 'Racha del Día',
            'description': 'Mantén tu racha diaria activa',
            'icon': '🔥',
            'challenge_type': 'daily',
            'category': 'streak',
            'target_action': 'maintain_streak',
            'target_count': 1,
            'points_reward': 25,
            'priority': 95
        },
        
        # WEEKLY CHALLENGES
        {
            'title': 'Guerrero de la Semana',
            'description': 'Aplica a 20 trabajos durante la semana',
            'icon': '⚔️',
            'challenge_type': 'weekly',
            'category': 'applications',
            'target_action': 'apply_to_jobs',
            'target_count': 20,
            'points_reward': 150,
            'priority': 70
        },
        {
            'title': 'Perfil Completo',
            'description': 'Completa el 100% de tu perfil',
            'icon': '⭐',
            'challenge_type': 'weekly',
            'category': 'profile',
            'target_action': 'complete_profile',
            'target_count': 1,
            'points_reward': 100,
            'priority': 75
        },
        {
            'title': 'Networking Pro',
            'description': 'Conéctate con 3 mentores esta semana',
            'icon': '🤝',
            'challenge_type': 'weekly',
            'category': 'networking',
            'target_action': 'connect_mentors',
            'target_count': 3,
            'points_reward': 120,
            'priority': 65
        },
        {
            'title': 'Estudiante Dedicado',
            'description': 'Inscríbete en 2 cursos recomendados',
            'icon': '📚',
            'challenge_type': 'weekly',
            'category': 'learning',
            'target_action': 'enroll_courses',
            'target_count': 2,
            'points_reward': 80,
            'priority': 60
        },
        {
            'title': 'Racha de Fuego',
            'description': 'Mantén una racha de 7 días consecutivos',
            'icon': '🔥',
            'challenge_type': 'weekly',
            'category': 'streak',
            'target_action': 'maintain_streak',
            'target_count': 7,
            'points_reward': 200,
            'bonus_multiplier': 1.5,
            'priority': 85
        },
        
        # SPECIAL CHALLENGES
        {
            'title': 'Bienvenido a JOBY',
            'description': 'Completa tu primer día en la plataforma',
            'icon': '🎉',
            'challenge_type': 'special',
            'category': 'exploration',
            'target_action': 'first_login',
            'target_count': 1,
            'points_reward': 30,
            'priority': 110
        },
        {
            'title': 'Maratonista de Aplicaciones',
            'description': 'Aplica a 50 trabajos en total',
            'icon': '🏃',
            'challenge_type': 'special',
            'category': 'applications',
            'target_action': 'apply_to_jobs',
            'target_count': 50,
            'points_reward': 300,
            'bonus_multiplier': 2.0,
            'priority': 50
        },
        {
            'title': 'Invita a un Amigo',
            'description': 'Refiere a tu primer amigo a JOBY',
            'icon': '🎁',
            'challenge_type': 'special',
            'category': 'networking',
            'target_action': 'refer_friend',
            'target_count': 1,
            'points_reward': 50,
            'priority': 88
        },
        {
            'title': 'Embajador JOBY',
            'description': 'Refiere a 5 amigos',
            'icon': '👑',
            'challenge_type': 'special',
            'category': 'networking',
            'target_action': 'refer_friend',
            'target_count': 5,
            'points_reward': 500,
            'bonus_multiplier': 3.0,
            'priority': 40
        },
    ]
    
    created_count = 0
    for data in challenges_data:
        challenge, created = Challenge.objects.get_or_create(
            title=data['title'],
            defaults=data
        )
        if created:
            print(f"✓ Reto creado: {challenge.icon} {challenge.title}")
            created_count += 1
        else:
            print(f"  Ya existe: {challenge.title}")
    
    return created_count


def complete_some_challenges_for_test_user():
    """Complete some challenges for test@test.com user"""
    
    try:
        user = User.objects.get(email='test@test.com')
    except User.DoesNotExist:
        print("❌ Usuario test@test.com no encontrado")
        return 0
    
    # Get some challenges to mark as completed
    challenges_to_complete = [
        'Bienvenido a JOBY',
        'Primera Aplicación del Día',
        'Actualiza tu Perfil',
        'Invita a un Amigo',
    ]
    
    completed_count = 0
    for title in challenges_to_complete:
        try:
            challenge = Challenge.objects.get(title=title)
            
            # Check if already completed
            existing = UserChallenge.objects.filter(
                user=user,
                challenge=challenge,
                status='completed'
            ).first()
            
            if not existing:
                # Create completed challenge
                user_challenge = UserChallenge.objects.create(
                    user=user,
                    challenge=challenge,
                    current_progress=challenge.target_count,
                    status='completed',
                    completed_at=date.today(),
                    points_earned=challenge.points_reward
                )
                
                # Award points to user
                user.points += challenge.points_reward
                user.save()
                
                print(f"✓ Reto completado para test user: {challenge.icon} {challenge.title} (+{challenge.points_reward} pts)")
                completed_count += 1
            else:
                print(f"  Ya completado: {title}")
        except Challenge.DoesNotExist:
            print(f"  Reto no encontrado: {title}")
    
    return completed_count


if __name__ == '__main__':
    print("=" * 60)
    print("CREANDO RETOS PARA SISTEMA DE RACHAS")
    print("=" * 60)
    
    created = create_challenges()
    print(f"\n✅ {created} retos nuevos creados")
    
    total_challenges = Challenge.objects.count()
    print(f"📊 Total de retos en sistema: {total_challenges}")
    
    print("\n" + "=" * 60)
    print("COMPLETANDO ALGUNOS RETOS PARA USUARIO TEST")
    print("=" * 60)
    
    completed = complete_some_challenges_for_test_user()
    print(f"\n✅ {completed} retos completados para test@test.com")
    
    print("\n" + "=" * 60)
    print("¡LISTO! Sistema de retos configurado")
    print("=" * 60)
