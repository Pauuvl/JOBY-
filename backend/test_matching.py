"""
Script para probar el algoritmo de matching y ver por qué no aparecen mentores
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'joby_api.settings')
django.setup()

from apps.users.models import User, SuccessStory
from apps.users.views_mentorship import calculate_profile_similarity

def test_matching():
    """Probar el matching de mentores"""
    
    try:
        # Obtener usuario test
        test_user = User.objects.get(email='test@test.com')
        print(f'\n👤 Usuario: {test_user.name}')
        print(f'   Email: {test_user.email}')
        print(f'   Skills: {test_user.skills}')
        print(f'   Location: {test_user.location}')
        print(f'   Experience: {test_user.experience}')
        
        # Obtener mentores disponibles
        mentors = User.objects.filter(
            success_story__is_willing_to_mentor=True,
            success_story__is_active=True
        ).exclude(id=test_user.id)
        
        print(f'\n🎯 Mentores disponibles: {mentors.count()}')
        print('\n' + '='*70)
        
        # Calcular match con cada mentor
        matches = []
        for mentor in mentors:
            score = calculate_profile_similarity(test_user, mentor)
            matches.append((mentor, score))
            
            print(f'\n✓ {mentor.name} - {mentor.success_story.position}')
            print(f'   Empresa: {mentor.success_story.company}')
            print(f'   Score: {score}%')
            print(f'   Skills mentor: {mentor.skills}')
            
            # Calcular skills en común
            test_skills = set([s.lower() for s in (test_user.skills or [])])
            mentor_skills = set([s.lower() for s in (mentor.skills or [])])
            common = test_skills.intersection(mentor_skills)
            print(f'   Skills comunes: {list(common)}')
            print(f'   Misma ubicación: {test_user.location == mentor.location}')
        
        print('\n' + '='*70)
        
        # Filtrar por score >= 30
        good_matches = [m for m in matches if m[1] >= 30]
        print(f'\n✅ Matches con score >= 30: {len(good_matches)}')
        
        if not good_matches:
            print('\n⚠️  NO HAY MATCHES suficientes (score < 30)')
            print('\nPosibles razones:')
            print('1. El usuario no tiene suficientes skills en común')
            print('2. El algoritmo necesita ajuste')
            
    except User.DoesNotExist:
        print('❌ Usuario test@test.com no encontrado')

if __name__ == '__main__':
    test_matching()
