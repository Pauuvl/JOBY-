"""
Script para actualizar el perfil de test@test.com y que tenga matches con mentores
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'joby_api.settings')
django.setup()

from apps.users.models import User

def update_test_user():
    """Actualizar usuario test@test.com para que tenga matches con mentores"""
    
    try:
        user = User.objects.get(email='test@test.com')
        
        print(f'\n📝 Actualizando perfil de: {user.name} ({user.email})')
        print(f'Skills actuales: {user.skills}')
        
        # Actualizar skills para que coincidan con los mentores
        # Agregamos skills que tienen los mentores para generar matches
        new_skills = [
            'Python',      # Coincide con María y Carlos
            'Django',      # Coincide con María
            'React',       # Coincide con Ana
            'JavaScript',  # Coincide con Ana
            'Node.js',     # Coincide con Ana
            'Kubernetes',  # Coincide con Laura
            'Docker',      # Coincide con María y Laura
            'AWS',         # Coincide con Ana
            'Machine Learning',  # Coincide con Carlos
            'Android',     # Coincide con Pedro
        ]
        
        user.skills = new_skills
        user.location = 'Madrid'  # Coincide con María y Laura
        user.experience = 'Junior Developer con 1 año de experiencia en desarrollo web'
        user.save()
        
        print(f'\n✅ Perfil actualizado exitosamente!')
        print(f'Nuevas skills: {user.skills}')
        print(f'Ubicación: {user.location}')
        print(f'Experiencia: {user.experience}')
        
        print(f'\n🎯 Matches esperados:')
        print(f'  - María García (Google) - Python, Django, Docker')
        print(f'  - Carlos Rodríguez (Microsoft) - Python, Machine Learning')
        print(f'  - Ana Martínez (Amazon) - React, Node.js, JavaScript, AWS')
        print(f'  - Pedro López (Meta) - Android')
        print(f'  - Laura Fernández (Netflix) - Kubernetes, Docker, ubicación Madrid')
        
    except User.DoesNotExist:
        print('❌ Usuario test@test.com no encontrado')
        print('Por favor, crea el usuario primero')

if __name__ == '__main__':
    update_test_user()
