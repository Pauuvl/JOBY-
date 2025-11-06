"""
Script para poblar la base de datos con compañías y cursos de prueba
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'joby_api.settings')
django.setup()

from apps.users.models import Company, Course

def create_companies():
    companies_data = [
        {
            'name': 'Google',
            'logo_url': 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png',
            'website': 'https://careers.google.com',
            'description': 'Líder mundial en tecnología, especializado en servicios de internet',
            'is_active': True
        },
        {
            'name': 'Microsoft',
            'logo_url': 'https://img-prod-cms-rt-microsoft-com.akamaized.net/cms/api/am/imageFileData/RE1Mu3b',
            'website': 'https://careers.microsoft.com',
            'description': 'Gigante tecnológico líder en software y servicios cloud',
            'is_active': True
        },
        {
            'name': 'Platzi',
            'logo_url': 'https://static.platzi.com/media/platzi-isotipo@2x.png',
            'website': 'https://platzi.com',
            'description': 'Plataforma de educación online en español',
            'is_active': True
        },
        {
            'name': 'Coursera',
            'logo_url': 'https://d3njjcbhbojbot.cloudfront.net/web/images/favicons/icon-blue-72x72.png',
            'website': 'https://www.coursera.org',
            'description': 'Plataforma global de aprendizaje online',
            'is_active': True
        },
        {
            'name': 'Udemy',
            'logo_url': 'https://www.udemy.com/staticx/udemy/images/v7/logo-udemy.svg',
            'website': 'https://www.udemy.com',
            'description': 'Plataforma de cursos online para profesionales',
            'is_active': True
        }
    ]
    
    companies = []
    for data in companies_data:
        company, created = Company.objects.get_or_create(
            name=data['name'],
            defaults=data
        )
        companies.append(company)
        if created:
            print(f'✓ Compañía creada: {company.name}')
        else:
            print(f'- Compañía existente: {company.name}')
    
    return companies

def create_courses(companies):
    google, microsoft, platzi, coursera, udemy = companies
    
    courses_data = [
        # Google courses
        {
            'title': 'Google Cloud Platform Fundamentals',
            'description': 'Aprende los fundamentos de Google Cloud Platform, incluyendo Compute Engine, Storage y Networking',
            'company': google,
            'required_skills': ['Python', 'Linux'],
            'skills_taught': ['GCP', 'Cloud Computing', 'Kubernetes', 'Docker'],
            'level': 'intermediate',
            'duration_value': 40,
            'duration_unit': 'hours',
            'course_url': 'https://cloud.google.com/training',
            'is_free': False,
            'price': 49.99,
            'currency': 'USD',
            'rating': 4.7,
            'enrollments': 15420,
            'priority': 90
        },
        {
            'title': 'Android Development with Kotlin',
            'description': 'Curso completo de desarrollo Android usando Kotlin y Jetpack Compose',
            'company': google,
            'required_skills': ['Java'],
            'skills_taught': ['Kotlin', 'Android', 'Mobile Development', 'Jetpack Compose'],
            'level': 'intermediate',
            'duration_value': 60,
            'duration_unit': 'hours',
            'course_url': 'https://developer.android.com/courses',
            'is_free': True,
            'rating': 4.8,
            'enrollments': 32100,
            'priority': 85
        },
        
        # Microsoft courses
        {
            'title': 'Azure Fundamentals',
            'description': 'Fundamentos de Microsoft Azure para desarrolladores y administradores de sistemas',
            'company': microsoft,
            'required_skills': ['Cloud basics'],
            'skills_taught': ['Azure', 'Cloud Computing', 'DevOps', 'CI/CD'],
            'level': 'beginner',
            'duration_value': 30,
            'duration_unit': 'hours',
            'course_url': 'https://learn.microsoft.com/azure',
            'is_free': True,
            'rating': 4.6,
            'enrollments': 28500,
            'priority': 95
        },
        {
            'title': '.NET Core Development',
            'description': 'Desarrollo de aplicaciones web modernas con .NET Core y C#',
            'company': microsoft,
            'required_skills': ['C#', 'OOP'],
            'skills_taught': ['.NET Core', 'ASP.NET', 'Entity Framework', 'Web APIs'],
            'level': 'intermediate',
            'duration_value': 50,
            'duration_unit': 'hours',
            'course_url': 'https://learn.microsoft.com/dotnet',
            'is_free': True,
            'rating': 4.7,
            'enrollments': 19800,
            'priority': 80
        },
        
        # Platzi courses
        {
            'title': 'Curso de Python desde Cero',
            'description': 'Aprende Python desde cero hasta nivel intermedio con proyectos prácticos',
            'company': platzi,
            'required_skills': [],
            'skills_taught': ['Python', 'Programming', 'Data Structures', 'OOP'],
            'level': 'beginner',
            'duration_value': 20,
            'duration_unit': 'hours',
            'course_url': 'https://platzi.com/cursos/python',
            'is_free': False,
            'price': 29.99,
            'currency': 'USD',
            'rating': 4.9,
            'enrollments': 45600,
            'priority': 100
        },
        {
            'title': 'React.js: De Cero a Experto',
            'description': 'Domina React.js con Hooks, Context API y React Router',
            'company': platzi,
            'required_skills': ['JavaScript', 'HTML', 'CSS'],
            'skills_taught': ['React', 'React Hooks', 'Redux', 'React Router'],
            'level': 'intermediate',
            'duration_value': 35,
            'duration_unit': 'hours',
            'course_url': 'https://platzi.com/cursos/react',
            'is_free': False,
            'price': 39.99,
            'currency': 'USD',
            'rating': 4.8,
            'enrollments': 38200,
            'priority': 90
        },
        {
            'title': 'Introducción a Machine Learning',
            'description': 'Fundamentos de Machine Learning con Python y scikit-learn',
            'company': platzi,
            'required_skills': ['Python', 'Mathematics'],
            'skills_taught': ['Machine Learning', 'scikit-learn', 'Data Science', 'AI'],
            'level': 'intermediate',
            'duration_value': 40,
            'duration_unit': 'hours',
            'course_url': 'https://platzi.com/cursos/machine-learning',
            'is_free': False,
            'price': 49.99,
            'currency': 'USD',
            'rating': 4.7,
            'enrollments': 22400,
            'priority': 85
        },
        
        # Coursera courses
        {
            'title': 'Full Stack Web Development',
            'description': 'Curso completo de desarrollo web full stack con Node.js y React',
            'company': coursera,
            'required_skills': ['JavaScript', 'HTML'],
            'skills_taught': ['Node.js', 'Express', 'React', 'MongoDB', 'Full Stack'],
            'level': 'intermediate',
            'duration_value': 80,
            'duration_unit': 'hours',
            'course_url': 'https://www.coursera.org/specializations/full-stack',
            'is_free': False,
            'price': 79.99,
            'currency': 'USD',
            'rating': 4.6,
            'enrollments': 31200,
            'priority': 80
        },
        {
            'title': 'Data Structures and Algorithms',
            'description': 'Estructuras de datos y algoritmos para entrevistas técnicas',
            'company': coursera,
            'required_skills': ['Python'],
            'skills_taught': ['Algorithms', 'Data Structures', 'Problem Solving', 'Technical Interviews'],
            'level': 'intermediate',
            'duration_value': 45,
            'duration_unit': 'hours',
            'course_url': 'https://www.coursera.org/learn/data-structures-algorithms',
            'is_free': False,
            'price': 59.99,
            'currency': 'USD',
            'rating': 4.8,
            'enrollments': 42500,
            'priority': 95
        },
        
        # Udemy courses
        {
            'title': 'The Complete JavaScript Course',
            'description': 'JavaScript moderno desde cero: ES6+, Async/Await, APIs y más',
            'company': udemy,
            'required_skills': [],
            'skills_taught': ['JavaScript', 'ES6+', 'Async Programming', 'Web APIs'],
            'level': 'beginner',
            'duration_value': 45,
            'duration_unit': 'hours',
            'course_url': 'https://www.udemy.com/course/javascript-complete',
            'is_free': False,
            'price': 19.99,
            'currency': 'USD',
            'rating': 4.7,
            'enrollments': 52300,
            'priority': 90
        },
        {
            'title': 'Docker y Kubernetes: Guía Práctica',
            'description': 'Aprende Docker y Kubernetes desde cero con proyectos reales',
            'company': udemy,
            'required_skills': ['Linux', 'Basic networking'],
            'skills_taught': ['Docker', 'Kubernetes', 'Containers', 'Microservices', 'DevOps'],
            'level': 'intermediate',
            'duration_value': 35,
            'duration_unit': 'hours',
            'course_url': 'https://www.udemy.com/course/docker-kubernetes',
            'is_free': False,
            'price': 24.99,
            'currency': 'USD',
            'rating': 4.8,
            'enrollments': 27800,
            'priority': 85
        },
        {
            'title': 'SQL para Data Science',
            'description': 'Domina SQL para análisis de datos y Business Intelligence',
            'company': udemy,
            'required_skills': [],
            'skills_taught': ['SQL', 'PostgreSQL', 'Data Analysis', 'Database Design'],
            'level': 'beginner',
            'duration_value': 25,
            'duration_unit': 'hours',
            'course_url': 'https://www.udemy.com/course/sql-data-science',
            'is_free': False,
            'price': 19.99,
            'currency': 'USD',
            'rating': 4.6,
            'enrollments': 34500,
            'priority': 75
        }
    ]
    
    courses = []
    for data in courses_data:
        course, created = Course.objects.get_or_create(
            title=data['title'],
            company=data['company'],
            defaults=data
        )
        courses.append(course)
        if created:
            print(f'✓ Curso creado: {course.title}')
        else:
            print(f'- Curso existente: {course.title}')
    
    return courses

def main():
    print('\n' + '='*60)
    print('POBLANDO BASE DE DATOS CON CURSOS')
    print('='*60 + '\n')
    
    print('Creando compañías...')
    companies = create_companies()
    print(f'\nTotal compañías: {len(companies)}\n')
    
    print('Creando cursos...')
    courses = create_courses(companies)
    print(f'\nTotal cursos: {len(courses)}\n')
    
    print('='*60)
    print('✓ BASE DE DATOS POBLADA EXITOSAMENTE')
    print('='*60)
    print(f'\nEstadísticas:')
    print(f'- Compañías: {Company.objects.count()}')
    print(f'- Cursos: {Course.objects.count()}')
    print(f'- Cursos gratuitos: {Course.objects.filter(is_free=True).count()}')
    print(f'- Cursos de pago: {Course.objects.filter(is_free=False).count()}')
    print()

if __name__ == '__main__':
    main()
