# 🚀 Joby - Tu Compañero de Búsqueda de Empleo

**Joby** es una aplicación móvil innovadora diseñada para revolucionar la búsqueda de empleo. Combina gamificación, inteligencia artificial y una experiencia de usuario excepcional para ayudar a los candidatos a encontrar su trabajo ideal de manera más efectiva y motivadora.

## ✨ Características Principales

### 📱 Experiencia de Usuario Completa
- **Búsqueda Inteligente**: Encuentra trabajos según tu perfil, habilidades y preferencias
- **Alertas de Trabajo Personalizadas**: Recibe notificaciones automáticas de trabajos que coinciden con tu perfil
- **Detalles Completos**: Visualiza toda la información de cada trabajo (descripción, requisitos, beneficios, salario)
- **Aplicación Rápida**: Aplica a trabajos con un solo click
- **Historial de Aplicaciones**: Seguimiento completo de tus postulaciones

### 🔥 Sistema de Gamificación Completo

#### 🎯 **Sistema de Retos y Desafíos**
Completa desafíos diarios, semanales y especiales para ganar puntos:
- **Retos Diarios** (10-50 puntos):
  - Primera Aplicación del Día
  - Aplicador Activo (5 aplicaciones)
  - Actualiza tu Perfil
  - Explorador (Ver 10 trabajos)
  - Racha del Día

- **Retos Semanales** (80-200 puntos):
  - Guerrero de la Semana (20 aplicaciones)
  - Perfil Completo (100% completado)
  - Networking Pro (Conectar con mentores)
  - Estudiante Dedicado (Completar cursos)
  - Racha de Fuego (7 días consecutivos)

- **Retos Especiales** (30-500 puntos):
  - Bienvenido a JOBY
  - Maratonista (50 aplicaciones)
  - Invita a un Amigo
  - Embajador JOBY (10 referidos)

#### 🎁 **Sistema de Recompensas**
Canjea tus puntos por recompensas exclusivas:
- **Insignias** (100-1000 puntos):
  - Badge Principiante, Experto, Maestro

- **Descuentos** (150-300 puntos):
  - 20% y 50% en cursos premium

- **Cursos Gratuitos** (250-500 puntos):
  - Acceso a cursos básicos y premium

- **Features Premium** (100-600 puntos):
  - Perfil Destacado (7 o 30 días)
  - Análisis de CV con IA

#### 👥 **Sistema de Referidos**
Invita amigos y gana puntos por cada etapa:
- **Registro completado**: +50 puntos
- **Perfil completado**: +100 puntos adicionales
- **Primer empleo conseguido**: +200 puntos adicionales
- **Tabla de clasificación**: Compite con otros usuarios

#### 🏆 **Rachas Diarias**
Mantén tu racha activa con actividades diarias:
- Ingreso diario: **+10 puntos**
- Aplicar a trabajos: **+20 puntos**
- Actualizar perfil: **+15 puntos**
- Sistema de notificaciones para mantener tu racha

### 📚 **Sistema de Cursos Recomendados**
- **12 Cursos Disponibles** de 5 empresas partner
- Recomendaciones personalizadas según tu perfil
- Filtros por nivel (Principiante, Intermedio, Avanzado)
- Duración y precio detallados
- Registro directo desde la app

### 🤝 **Sistema de Mentoría**
- **Encuentra Mentores** según tu perfil profesional
- Algoritmo de matching inteligente
- Solicitudes de mentoría directas
- Perfiles detallados de mentores con experiencia y áreas de expertise



### 🔔 **Sistema de Notificaciones**
- Notificaciones de nuevos trabajos compatibles
- Alertas de aplicaciones exitosas
- Recordatorios de rachas y retos
- Actualizaciones de mentores y cursos
- Sistema de limpieza masiva de notificaciones

### 👤 Perfil Personalizable
- Edita tu información personal completa
- Sistema de habilidades con agregar/eliminar
- Experiencia laboral detallada
- Información académica
- Enlaces sociales (LinkedIn, GitHub, Portfolio)
- Foto de perfil personalizable
- Visualización de puntos acumulados
- Acceso rápido a:
  - 🔥 Rachas
  - 📚 Cursos Recomendados
  - 🤝 Mentores
  - 🎁 Sistema de Referidos

### 📊 Estadísticas y Seguimiento
- Historial completo de aplicaciones con estados
- Trabajos guardados y favoritos
- Progreso de rachas diarias
- Puntos totales y ranking
- Historial de transacciones de puntos
- Retos completados y pendientes
- Recompensas canjeadas

## 🛠️ Tecnologías (Stack Completo)

### Frontend (✅ Implementado)
- **Flutter 3.9+** - Framework multiplataforma
- **Dart 3.0+** - Lenguaje de programación
- **Provider** - Gestión de estado
- **HTTP** - Peticiones a la API
- **Shared Preferences** - Almacenamiento local
- **Flutter Secure Storage** - Almacenamiento seguro de tokens

### Backend (✅ Implementado)
- **Django 4.2.9** - Framework web
- **Django REST Framework** - API REST
- **PostgreSQL** - Base de datos relacional
- **psycopg3** - Conector PostgreSQL (soporte UTF-8 mejorado)
- **JWT (djangorestframework-simplejwt)** - Autenticación segura
- **Celery** - Tareas asíncronas
- **Django Celery Beat** - Tareas programadas

### Inteligencia Artificial (✅ Implementado)
- **OpenAI API (GPT-4)** - Chatbot inteligente
- Asistente personalizado para búsqueda de empleo
- Recomendaciones de cursos y mentores

### Notificaciones (✅ Implementado)
- **Sistema de notificaciones interno** - Totalmente funcional
- Notificaciones automáticas de trabajos compatibles
- Alertas de rachas y retos
- Comando de envío masivo: `python manage.py send_job_alerts --all --create-jobs`

### DevOps (🚧 En progreso)
- **Git/GitHub** - Control de versiones
- **Python venv** - Entornos virtuales
- **Docker** (planeado) - Containerización

## 🚀 Instalación y Uso

### Prerrequisitos
```bash
# Frontend
Flutter SDK 3.9 o superior
Dart SDK 3.0 o superior
Android Studio / VS Code

# Backend
Python 3.11+
PostgreSQL 15+
```

### Clonar el Repositorio
```bash
git clone https://github.com/Pauuvl/JOBY-.git
cd JOBY-
```

### Configurar Backend

1. **Crear y activar entorno virtual**:
```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno**:
Crear archivo `.env` en la carpeta `backend/`:
```env
# Django Settings
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL Database
DB_NAME=joby_db
DB_USER=postgres
DB_PASSWORD=tu-contraseña-postgres
DB_HOST=127.0.0.1
DB_PORT=5432

# JWT Authentication
JWT_SECRET_KEY=tu-jwt-secret-key
ACCESS_TOKEN_LIFETIME_MINUTES=60



4. **Crear base de datos PostgreSQL**:
```bash
# Opción 1: Usando Python
python recreate_db.py

# Opción 2: Usando psql
psql -U postgres
CREATE DATABASE joby_db;
\q
```

5. **Aplicar migraciones**:
```bash
python manage.py migrate
```

6. **Importar datos iniciales** (opcional - incluye usuarios, cursos, mentores, retos):
```bash
python import_data.py
```

7. **Poblar datos** (alternativa - crea datos desde cero):
```bash
python populate_challenges.py  # 14 retos
python populate_rewards.py     # 10 recompensas
python populate_courses.py     # 12 cursos
python populate_mentors.py     # 5 mentores
```

8. **Ejecutar servidor**:
```bash
python manage.py runserver 0.0.0.0:8000
```

### Configurar Frontend

1. **Instalar dependencias Flutter**:
```bash
cd ..  # Volver a raíz del proyecto
flutter pub get
```

2. **Configurar URL del backend**:
Editar `lib/services/*.dart` y actualizar la URL base si es necesario:
```dart
final String baseUrl = 'http://tu-ip:8000/api';
```

3. **Ejecutar la aplicación**:
```bash
# Desarrollo
flutter run

# Seleccionar dispositivo
flutter run -d chrome  # Web
flutter run -d windows # Windows desktop
```

### Compilar para Producción
```bash
# Android
flutter build apk --release

# iOS
flutter build ios --release

# Web
flutter build web --release
```

## 📂 Estructura del Proyecto

```
JOBY-/
├── backend/                              # Backend Django
│   ├── apps/
│   │   ├── applications/                # App de aplicaciones a trabajos   
│   │   ├── jobs/                        # Gestión de trabajos
│   │   ├── notifications/               # Sistema de notificaciones
│   │   ├── streaks/                     # Rachas y gamificación
│   │   └── users/                       # Usuarios y autenticación
│   │       ├── models.py               # User, JobAlertPreference
│   │       ├── models_courses.py       # Company, Course, UserCourse
│   │       ├── models_mentorship.py    # SuccessStory, ProfileMatch, MentorshipRequest
│   │       ├── models_referral.py      # ReferralCode, Referral, Reward, PointsTransaction
│   │       ├── serializers.py          # Serializadores principales
│   │       ├── serializers_courses.py  # Serializadores de cursos
│   │       ├── serializers_mentorship.py # Serializadores de mentoría
│   │       ├── serializers_referral.py # Serializadores de referidos
│   │       ├── views.py                # Vistas principales
│   │       ├── views_courses.py        # Vistas de cursos
│   │       ├── views_mentorship.py     # Vistas de mentoría
│   │       └── views_referral.py       # Vistas de referidos
│   ├── joby_api/
│   │   ├── settings.py                 # Configuración Django (PostgreSQL)
│   │   ├── urls.py                     # URLs principales
│   │   └── celery.py                   # Configuración Celery
│   ├── manage.py
│   ├── requirements.txt                # Dependencias Python
│   ├── .env                            # Variables de entorno
│   ├── backup_data.json                # Backup completo de datos
│   ├── export_data.py                  # Script de exportación
│   ├── import_data.py                  # Script de importación
│   ├── recreate_db.py                  # Recrear base de datos
│   ├── populate_challenges.py          # Poblar 14 retos
│   ├── populate_rewards.py             # Poblar 10 recompensas
│   ├── populate_courses.py             # Poblar 12 cursos
│   └── populate_mentors.py             # Poblar 5 mentores
│
├── lib/                                 # Frontend Flutter
│   ├── main.dart                       # Punto de entrada
│   ├── config/
│   │   └── theme.dart                  # Tema de la app
│   ├── models/                         # Modelos de datos
│   │   ├── job.dart
│   │   ├── user.dart
│   │   ├── streak.dart
│   │   ├── notification.dart
│   │   ├── course.dart
│   │   ├── mentor.dart
│   │   └── referral.dart               # 9 modelos de referidos
│   ├── providers/
│   │   └── user_provider.dart          # Gestión de estado
│   ├── screens/                        # Pantallas de la app
│   │   ├── login_screen.dart
│   │   ├── register_screen.dart
│   │   ├── home_screen.dart
│   │   ├── job_search_screen.dart
│   │   ├── job_detail_screen.dart
│   │   ├── profile_screen.dart
│   │   ├── edit_profile_screen.dart
│   │   ├── streak_screen.dart
│   │   ├── notifications_screen.dart
│   │   ├── courses_screen.dart
│   │   ├── mentors_screen.dart
│   │   ├── referral_screen.dart        # 3 tabs: Mi Código, Referidos, Ranking
│   │   
│   └── services/                       # Servicios y API
│       ├── auth_service.dart
│       ├── job_service.dart
│       ├── streak_service.dart
│       ├── notification_service.dart
│       ├── course_service.dart
│       ├── mentor_service.dart
│       ├── referral_service.dart       # 10 métodos API
│       
│
├── pubspec.yaml                        # Dependencias Flutter
├── README.md                           # Este archivo
└── comandos.md                         # Comandos útiles
```

## 🎯 Roadmap

### Fase 1: MVP Frontend ✅ (Completado)
- [x] Sistema de navegación completo
- [x] Búsqueda y listado de trabajos
- [x] Detalles de trabajos
- [x] Perfil de usuario editable
- [x] Sistema de rachas
- [x] Pantalla de notificaciones
- [x] Integración con backend

### Fase 2: Backend y Base de Datos ✅ (Completado)
- [x] API REST con Django REST Framework
- [x] Base de datos PostgreSQL
- [x] Autenticación JWT
- [x] Endpoints CRUD para trabajos y usuarios
- [x] Sistema de aplicaciones a trabajos
- [x] Sistema de alertas automáticas
- [x] Migraciones completadas (7 migraciones)

### Fase 3: Gamificación ✅ (Completado)
- [x] Sistema de rachas diarias
- [x] 14 Retos (diarios, semanales, especiales)
- [x] 10 Recompensas canjeables
- [x] Sistema de puntos
- [x] Historial de transacciones
- [x] Sistema de referidos completo
- [x] Tabla de clasificación
- [x] Compartir códigos de referido

### Fase 4: Contenido Educativo ✅ (Completado)
- [x] 12 Cursos de 5 empresas
- [x] Sistema de recomendación de cursos
- [x] Filtros por nivel y categoría
- [x] Registro a cursos
- [x] 5 Mentores disponibles
- [x] Sistema de matching inteligente
- [x] Solicitudes de mentoría

### Fase 5: Notificaciones ✅ (Completado)
- [x] Sistema de notificaciones interno
- [x] Notificaciones de trabajos compatibles
- [x] Alertas de aplicaciones
- [x] Recordatorios de rachas
- [x] Limpieza masiva de notificaciones

## 📊 Base de Datos

### Modelos Implementados (7 Migraciones)

**apps.users:**
- `User` - Modelo de usuario personalizado (UUID, puntos, perfil completo)
- `JobAlertPreference` - Preferencias de alertas de trabajo
- `Company` - Empresas que ofrecen cursos
- `Course` - Cursos disponibles
- `UserCourse` - Inscripciones a cursos
- `SuccessStory` - Historias de éxito de mentores
- `ProfileMatch` - Matching de perfiles para mentoría
- `MentorshipRequest` - Solicitudes de mentoría
- `ReferralCode` - Códigos de referido únicos
- `Referral` - Registros de usuarios referidos
- `PointsTransaction` - Historial de movimientos de puntos
- `Reward` - Catálogo de recompensas
- `RewardRedemption` - Canjes de recompensas

**apps.jobs:**
- `Job` - Ofertas de trabajo

**apps.applications:**
- `Application` - Aplicaciones a trabajos

**apps.notifications:**
- `Notification` - Notificaciones del sistema

**apps.streaks:**
- `Streak` - Rachas de usuarios
- `Achievement` - Logros desbloqueados
- `Challenge` - Retos disponibles
- `UserChallenge` - Retos completados por usuarios
- `PointsHistory` - Historial de puntos (legacy)

### Datos Iniciales Disponibles
- **12 Usuarios** (incluyendo usuario de prueba)
- **5 Mentores** con historias de éxito
- **12 Cursos** de 5 empresas
- **14 Retos** (5 diarios, 5 semanales, 4 especiales)
- **10 Recompensas** (badges, descuentos, cursos, features premium)
- **Archivo de backup completo**: `backend/backup_data.json` (94 registros)

## 🔧 Comandos Útiles

### Backend
```bash
# Activar entorno virtual
.\venv\Scripts\activate  # Windows
source venv/bin/activate # Linux/Mac

# Ejecutar servidor
python manage.py runserver 0.0.0.0:8000

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Enviar alertas de trabajo a todos los usuarios
python manage.py send_job_alerts --all --create-jobs

# Exportar datos
python export_data.py

# Importar datos
python import_data.py

# Poblar datos iniciales
python populate_challenges.py
python populate_rewards.py
python populate_courses.py
python populate_mentors.py

# Recrear base de datos
python recreate_db.py
```

### Frontend
```bash
# Instalar dependencias
flutter pub get

# Ejecutar en desarrollo
flutter run

# Ejecutar en web
flutter run -d chrome

# Limpiar caché
flutter clean

# Compilar para producción
flutter build apk --release      # Android
flutter build ios --release      # iOS
flutter build web --release      # Web
```

## 🔐 API Endpoints

### Autenticación
- `POST /api/auth/register/` - Registro de usuario
- `POST /api/auth/login/` - Login (JWT)
- `POST /api/auth/logout/` - Logout
- `GET /api/auth/profile/` - Obtener perfil
- `PUT /api/auth/profile/` - Actualizar perfil

### Trabajos
- `GET /api/jobs/` - Listar trabajos
- `GET /api/jobs/{id}/` - Detalle de trabajo
- `POST /api/jobs/` - Crear trabajo (admin)

### Aplicaciones
- `GET /api/applications/` - Mis aplicaciones
- `POST /api/applications/` - Aplicar a trabajo

### Notificaciones
- `GET /api/notifications/` - Mis notificaciones
- `POST /api/notifications/{id}/mark-as-read/` - Marcar como leída
- `POST /api/notifications/clear-all/` - Limpiar todas

### Rachas y Gamificación
- `GET /api/streaks/current/` - Mi racha actual
- `POST /api/streaks/check-in/` - Registrar check-in
- `GET /api/streaks/challenges/` - Retos disponibles
- `GET /api/streaks/my-challenges/` - Mis retos

### Cursos
- `GET /api/auth/courses/` - Cursos disponibles
- `GET /api/auth/courses/recommended/` - Cursos recomendados
- `POST /api/auth/courses/{id}/enroll/` - Inscribirse a curso

### Mentoría
- `GET /api/auth/mentorship/mentors/` - Mentores disponibles
- `GET /api/auth/mentorship/match/` - Mejores matches
- `POST /api/auth/mentorship/request/` - Solicitar mentoría

### Sistema de Referidos
- `GET /api/auth/referral/my_code/` - Mi código de referido
- `GET /api/auth/referral/my_referrals/` - Mis referidos
- `GET /api/auth/referral/stats/` - Estadísticas de referidos
- `GET /api/auth/referral/leaderboard/` - Tabla de clasificación

### Puntos y Recompensas
- `GET /api/auth/points/balance/` - Mi saldo de puntos
- `GET /api/auth/points/history/` - Historial de puntos
- `GET /api/auth/points/rewards/` - Recompensas disponibles
- `POST /api/auth/points/redeem/` - Canjear recompensa
- `GET /api/auth/points/my_redemptions/` - Mis canjes




## � Migración a Otro PC

### Exportar desde PC Actual
1. **Hacer commit del código**:
```bash
git add .
git commit -m "Versión completa con PostgreSQL"
git push origin main
```

2. **Backup de datos** (ya disponible):
```bash
# El archivo backup_data.json ya contiene todos los datos (94 registros)
# Incluye: 12 usuarios, 5 mentores, 12 cursos, 14 retos, 10 recompensas
```

### Importar en PC Nuevo
1. **Clonar repositorio**:
```bash
git clone https://github.com/Pauuvl/JOBY-.git
cd JOBY-
```

2. **Instalar PostgreSQL** (versión 15+)

3. **Configurar backend**:
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

4. **Configurar `.env`** con las credenciales del nuevo PC

5. **Recrear base de datos**:
```bash
python recreate_db.py
```

6. **Aplicar migraciones**:
```bash
python manage.py migrate
```

7. **Importar datos**:
```bash
python import_data.py
```

8. **Iniciar servidor**:
```bash
python manage.py runserver 0.0.0.0:8000
```

**¡Listo!** El proyecto estará funcionando con todos los datos en menos de 10 minutos.

## 🎨 Diseño

El diseño de Joby se inspira en:
- **Material Design 3** para consistencia visual
- **Apps de gamificación** como Duolingo (sistema de rachas)
- **Plataformas de empleo** modernas como LinkedIn
- **Concepto P-03 "Streak: Mobile Service"** de Magneto
- **Interfaz limpia y minimalista** con foco en usabilidad## 📈 Estadísticas del Proyecto

- **94 registros** en la base de datos
- **7 migraciones** aplicadas
- **10+ pantallas** implementadas en Flutter
- **40+ endpoints** API REST
- **14 retos** gamificados
- **10 recompensas** canjeables
- **12 cursos** educativos
- **5 mentores** disponibles
- **Sistema completo** de puntos y referidos


## 🤝 Contribuir

Este es un proyecto académico. Si deseas contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto es parte de un trabajo académico.

## 👥 Autores

- **Cristian Cabarcas** - Backend Lead & PostgreSQL Migration
- **Paulina Velazquez** - Frontend Lead & UI/UX
- **Yilmar Murillo** - Full Stack Developer
- **Fabian Buritica** - Backend Developer

## 🙏 Agradecimientos

- **OpenAI** por la API de GPT-4
- **Magneto** por el concepto de "Streak: Mobile Service" (P-03)
- **Django & Flutter communities** por la documentación y soporte
- **PostgreSQL** por la robustez de la base de datos

## 📧 Contacto

Para preguntas o sugerencias sobre el proyecto:
- GitHub: [@Pauuvl](https://github.com/Pauuvl)
- Repositorio: [JOBY-](https://github.com/Pauuvl/JOBY-)

---

**¿Listo para encontrar tu próximo trabajo? ¡Descarga Joby y comienza tu racha hoy! 🔥**

*Versión actual: 2.0 - PostgreSQL Migration Complete*
*Última actualización: Noviembre 2025*
