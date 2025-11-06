"""
Script to populate rewards and referral codes
Run: python populate_rewards.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'joby_api.settings')
django.setup()

from apps.users.models_referral import Reward, ReferralCode
from apps.users.views_referral import award_points
from django.contrib.auth import get_user_model

User = get_user_model()


def create_rewards():
    """Create reward catalog"""
    
    rewards_data = [
        # Badges
        {
            'name': 'Insignia Principiante',
            'description': 'Completa tu perfil y aplica a 10 trabajos',
            'reward_type': 'badge',
            'points_required': 100,
            'icon': '🥉',
            'max_redemptions_per_user': 1
        },
        {
            'name': 'Insignia Experto',
            'description': 'Aplica a 50 trabajos y conecta con 3 mentores',
            'reward_type': 'badge',
            'points_required': 500,
            'icon': '🥈',
            'max_redemptions_per_user': 1
        },
        {
            'name': 'Insignia Maestro',
            'description': 'Insignia exclusiva para los top performers',
            'reward_type': 'badge',
            'points_required': 1000,
            'icon': '🥇',
            'max_redemptions_per_user': 1
        },
        
        # Course Discounts
        {
            'name': '20% Descuento en Curso',
            'description': 'Obtén 20% de descuento en cualquier curso de la plataforma',
            'reward_type': 'course_discount',
            'points_required': 150,
            'icon': '🎓',
            'max_redemptions_per_user': 3
        },
        {
            'name': '50% Descuento en Curso',
            'description': 'Obtén 50% de descuento en cualquier curso',
            'reward_type': 'course_discount',
            'points_required': 300,
            'icon': '📚',
            'max_redemptions_per_user': 2
        },
        
        # Free Courses
        {
            'name': 'Curso Gratis (Básico)',
            'description': 'Acceso completo a un curso básico gratis',
            'reward_type': 'course_free',
            'points_required': 250,
            'icon': '🆓',
            'max_redemptions_per_user': 2
        },
        {
            'name': 'Curso Gratis (Premium)',
            'description': 'Acceso completo a un curso premium gratis',
            'reward_type': 'course_free',
            'points_required': 500,
            'icon': '⭐',
            'max_redemptions_per_user': 1
        },
        
        # Premium Features
        {
            'name': 'Perfil Destacado (7 días)',
            'description': 'Destaca tu perfil por 7 días para que reclutadores te encuentren fácilmente',
            'reward_type': 'premium_feature',
            'points_required': 200,
            'icon': '✨',
            'max_redemptions_per_user': 5
        },
        {
            'name': 'Perfil Destacado (30 días)',
            'description': 'Destaca tu perfil por 30 días',
            'reward_type': 'premium_feature',
            'points_required': 600,
            'icon': '🌟',
            'max_redemptions_per_user': 3
        },
        {
            'name': 'Análisis de CV por IA',
            'description': 'Recibe un análisis detallado de tu CV con sugerencias de mejora',
            'reward_type': 'premium_feature',
            'points_required': 100,
            'icon': '🤖',
            'max_redemptions_per_user': 3
        },
    ]
    
    created_count = 0
    for data in rewards_data:
        reward, created = Reward.objects.get_or_create(
            name=data['name'],
            defaults=data
        )
        if created:
            print(f"✓ Recompensa creada: {reward.icon} {reward.name} ({reward.points_required} pts)")
            created_count += 1
        else:
            print(f"  Ya existe: {reward.name}")
    
    return created_count


def setup_test_user():
    """Setup referral code and give welcome bonus to test user"""
    
    try:
        user = User.objects.get(email='test@test.com')
    except User.DoesNotExist:
        print("❌ Usuario test@test.com no encontrado")
        return False
    
    # Create referral code if doesn't exist
    referral_code, created = ReferralCode.objects.get_or_create(
        user=user
    )
    
    if created:
        print(f"✓ Código de referido creado: {referral_code.code}")
    else:
        print(f"  Código de referido existente: {referral_code.code}")
    
    # Give welcome bonus if new user (no points yet)
    if user.points == 0:
        award_points(
            user=user,
            transaction_type='welcome_bonus',
            points=20,
            description='Bono de bienvenida a JOBY'
        )
        print(f"✓ Bono de bienvenida otorgado: +20 puntos")
    
    print(f"\n📊 Puntos totales de {user.name}: {user.points}")
    print(f"🔗 Código de referido: {referral_code.code}")
    print(f"📱 Link de invitación: https://joby.app/register?ref={referral_code.code}")
    
    return True


if __name__ == '__main__':
    print("=" * 60)
    print("CREANDO CATÁLOGO DE RECOMPENSAS")
    print("=" * 60)
    
    created = create_rewards()
    print(f"\n✅ {created} recompensas nuevas creadas")
    
    total_rewards = Reward.objects.count()
    print(f"📊 Total de recompensas disponibles: {total_rewards}")
    
    print("\n" + "=" * 60)
    print("CONFIGURANDO USUARIO TEST")
    print("=" * 60)
    
    setup_test_user()
    
    print("\n" + "=" * 60)
    print("¡LISTO! Sistema de referidos configurado")
    print("=" * 60)
