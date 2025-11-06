"""
Script para poblar la base de datos con historias de éxito de prueba
"""
import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'joby_api.settings')
django.setup()

from apps.users.models import User, SuccessStory

def create_success_stories():
    """Crear historias de éxito para usuarios de prueba"""
    
    # Buscar usuarios existentes o crearlos
    users_data = [
        {
            'username': 'maria_dev',
            'email': 'maria@example.com',
            'name': 'María García',
            'location': 'Madrid',
            'skills': ['Python', 'Django', 'React', 'PostgreSQL', 'Docker'],
            'experience': 'Senior Developer con 5 años de experiencia',
        },
        {
            'username': 'carlos_data',
            'email': 'carlos@example.com',
            'name': 'Carlos Rodríguez',
            'location': 'Barcelona',
            'skills': ['Python', 'Machine Learning', 'TensorFlow', 'Data Science', 'SQL'],
            'experience': 'Data Scientist con 4 años de experiencia',
        },
        {
            'username': 'ana_fullstack',
            'email': 'ana@example.com',
            'name': 'Ana Martínez',
            'location': 'Valencia',
            'skills': ['JavaScript', 'React', 'Node.js', 'MongoDB', 'AWS'],
            'experience': 'Full Stack Developer con 3 años de experiencia',
        },
        {
            'username': 'pedro_mobile',
            'email': 'pedro@example.com',
            'name': 'Pedro López',
            'location': 'Sevilla',
            'skills': ['Kotlin', 'Android', 'Java', 'Firebase', 'REST APIs'],
            'experience': 'Mobile Developer con 4 años de experiencia',
        },
        {
            'username': 'laura_cloud',
            'email': 'laura@example.com',
            'name': 'Laura Fernández',
            'location': 'Madrid',
            'skills': ['Azure', 'Kubernetes', 'Docker', 'DevOps', 'CI/CD'],
            'experience': 'Cloud Architect con 6 años de experiencia',
        },
    ]
    
    stories_data = [
        {
            'company': 'Google',
            'position': 'Senior Software Engineer',
            'hire_date': date.today() - timedelta(days=180),
            'salary_range': '100k+',
            'is_willing_to_mentor': True,
            'max_mentees': 3,
            'success_description': 'Conseguí el trabajo después de 6 meses de preparación intensiva. '
                'Lo clave fue practicar algoritmos todos los días y hacer proyectos de código abierto. '
                'Las entrevistas fueron difíciles pero la preparación valió la pena. '
                '¡No te rindas!',
            'key_skills_used': ['Python', 'Django', 'Algorithms', 'System Design'],
        },
        {
            'company': 'Microsoft',
            'position': 'Data Scientist',
            'hire_date': date.today() - timedelta(days=120),
            'salary_range': '70k-100k',
            'is_willing_to_mentor': True,
            'max_mentees': 2,
            'success_description': 'Mi consejo: construye un portafolio sólido con proyectos de ML reales. '
                'Participa en Kaggle y contribuye a proyectos open source. '
                'La persistencia es clave, apliqué a más de 50 posiciones antes de conseguir esta.',
            'key_skills_used': ['Machine Learning', 'Python', 'TensorFlow', 'Statistics'],
        },
        {
            'company': 'Amazon',
            'position': 'Full Stack Developer',
            'hire_date': date.today() - timedelta(days=90),
            'salary_range': '70k-100k',
            'is_willing_to_mentor': True,
            'max_mentees': 4,
            'success_description': 'Estudié todos los días durante 4 meses. Lo más importante fue '
                'tener proyectos full stack completos en mi GitHub. También practiqué mucho '
                'las preguntas de behavioral interviews. ¡Tú también puedes lograrlo!',
            'key_skills_used': ['React', 'Node.js', 'AWS', 'Microservices'],
        },
        {
            'company': 'Meta',
            'position': 'Android Developer',
            'hire_date': date.today() - timedelta(days=60),
            'salary_range': '70k-100k',
            'is_willing_to_mentor': True,
            'max_mentees': 3,
            'success_description': 'Construí 5 apps completas y las publiqué en Play Store. '
                'Esto fue crucial para demostrar mis habilidades. También contribuí a '
                'bibliotecas de Android open source. El networking también ayudó mucho.',
            'key_skills_used': ['Kotlin', 'Android', 'Jetpack Compose', 'MVVM'],
        },
        {
            'company': 'Netflix',
            'position': 'Cloud Engineer',
            'hire_date': date.today() - timedelta(days=150),
            'salary_range': '100k+',
            'is_willing_to_mentor': True,
            'max_mentees': 2,
            'success_description': 'Obtuve certificaciones de Azure y AWS. Monté un laboratorio '
                'personal en la nube donde experimenté con Kubernetes y CI/CD. '
                'Documenté todo en un blog técnico que me ayudó mucho en las entrevistas.',
            'key_skills_used': ['Azure', 'Kubernetes', 'Terraform', 'DevOps'],
        },
    ]
    
    print('\n' + '='*60)
    print('CREANDO HISTORIAS DE ÉXITO')
    print('='*60 + '\n')
    
    for user_data, story_data in zip(users_data, stories_data):
        # Crear o obtener usuario
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'name': user_data['name'],
                'location': user_data['location'],
                'skills': user_data['skills'],
                'experience': user_data['experience'],
            }
        )
        
        if created:
            user.set_password('password123')
            user.save()
            print(f'✓ Usuario creado: {user.name}')
        else:
            # Actualizar skills si el usuario ya existe
            user.skills = user_data['skills']
            user.location = user_data['location']
            user.experience = user_data['experience']
            user.save()
            print(f'- Usuario actualizado: {user.name}')
        
        # Crear historia de éxito
        story, story_created = SuccessStory.objects.get_or_create(
            user=user,
            defaults={
                **story_data,
            }
        )
        
        if story_created:
            print(f'  ✓ Historia: {story.position} en {story.company}')
        else:
            # Actualizar historia
            for key, value in story_data.items():
                setattr(story, key, value)
            story.save()
            print(f'  - Historia actualizada: {story.position} en {story.company}')
    
    print('\n' + '='*60)
    print('✓ HISTORIAS DE ÉXITO CREADAS')
    print('='*60)
    print(f'\nEstadísticas:')
    print(f'- Total usuarios: {User.objects.count()}')
    print(f'- Historias de éxito: {SuccessStory.objects.count()}')
    print(f'- Mentores disponibles: {SuccessStory.objects.filter(is_willing_to_mentor=True).count()}')
    print()
    
    print('Credenciales de acceso:')
    for user_data in users_data:
        print(f'  - Usuario: {user_data["username"]} | Password: password123')
    print()

if __name__ == '__main__':
    create_success_stories()
