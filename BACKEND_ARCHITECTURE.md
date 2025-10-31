# Backend Django - Joby API

## Estructura del Backend

```
backend/
├── manage.py
├── requirements.txt
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── joby_api/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── users/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── jobs/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── applications/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── streaks/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   └── chatbot/
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       └── urls.py
└── tests/
```

## Modelos de Base de Datos (PostgreSQL)

### User (Extendido de AbstractUser)
```python
- id (UUID, PK)
- email (EmailField, unique)
- password (CharField, hashed)
- name (CharField)
- phone (CharField, optional)
- profile_image_url (URLField, optional)
- resume_url (URLField, optional)
- experience (TextField, optional)
- education (TextField, optional)
- location (CharField, optional)
- skills (JSONField, array of strings)
- is_active (BooleanField, default=True)
- created_at (DateTimeField, auto_now_add)
- updated_at (DateTimeField, auto_now)
```

### Job
```python
- id (UUID, PK)
- title (CharField)
- company (CharField)
- location (CharField)
- salary (CharField)
- description (TextField)
- requirements (TextField)
- benefits (TextField)
- type (CharField, choices: Remote/Hybrid/On-site)
- status (CharField, choices: Open/Closed/Paused)
- posted_date (DateTimeField)
- expiry_date (DateTimeField, optional)
- created_by (ForeignKey to User, optional)
- created_at (DateTimeField, auto_now_add)
- updated_at (DateTimeField, auto_now)
```

### Application
```python
- id (UUID, PK)
- user (ForeignKey to User)
- job (ForeignKey to Job)
- status (CharField, choices: Pending/Reviewed/Accepted/Rejected)
- cover_letter (TextField, optional)
- applied_at (DateTimeField, auto_now_add)
- updated_at (DateTimeField, auto_now)
```

### Streak
```python
- id (UUID, PK)
- user (OneToOneField to User)
- current_streak (IntegerField, default=0)
- longest_streak (IntegerField, default=0)
- total_points (IntegerField, default=0)
- last_activity_date (DateTimeField)
- created_at (DateTimeField, auto_now_add)
- updated_at (DateTimeField, auto_now)
```

### Activity
```python
- id (UUID, PK)
- streak (ForeignKey to Streak)
- type (CharField, choices: job_applied/profile_updated/daily_login/friend_referred)
- description (CharField)
- points (IntegerField)
- created_at (DateTimeField, auto_now_add)
```

### Badge
```python
- id (UUID, PK)
- streak (ForeignKey to Streak)
- badge_id (CharField)
- name (CharField)
- description (TextField)
- icon (CharField)
- earned_date (DateTimeField, auto_now_add)
```

### SavedJob (Favoritos)
```python
- id (UUID, PK)
- user (ForeignKey to User)
- job (ForeignKey to Job)
- created_at (DateTimeField, auto_now_add)
- unique_together = ('user', 'job')
```

### ChatMessage
```python
- id (UUID, PK)
- user (ForeignKey to User)
- message (TextField)
- response (TextField)
- context (JSONField, optional)
- created_at (DateTimeField, auto_now_add)
```

## Endpoints API

### Autenticación
```
POST   /api/auth/register/          - Registro de usuario
POST   /api/auth/login/             - Login (obtener token JWT)
POST   /api/auth/refresh/           - Refrescar token
POST   /api/auth/logout/            - Logout
GET    /api/auth/me/                - Obtener usuario actual
```

### Usuarios
```
GET    /api/users/                  - Listar usuarios (admin)
GET    /api/users/{id}/             - Detalle de usuario
PUT    /api/users/{id}/             - Actualizar usuario
DELETE /api/users/{id}/             - Eliminar usuario
POST   /api/users/upload-resume/    - Subir CV
POST   /api/users/upload-photo/     - Subir foto de perfil
```

### Trabajos
```
GET    /api/jobs/                   - Listar trabajos (con paginación y filtros)
GET    /api/jobs/{id}/              - Detalle de trabajo
POST   /api/jobs/                   - Crear trabajo (admin/empresa)
PUT    /api/jobs/{id}/              - Actualizar trabajo
DELETE /api/jobs/{id}/              - Eliminar trabajo
GET    /api/jobs/search?q=          - Búsqueda de trabajos
GET    /api/jobs/recommended/       - Trabajos recomendados (basado en perfil)
```

### Aplicaciones
```
GET    /api/applications/           - Listar mis aplicaciones
GET    /api/applications/{id}/      - Detalle de aplicación
POST   /api/applications/           - Aplicar a un trabajo
PUT    /api/applications/{id}/      - Actualizar aplicación
DELETE /api/applications/{id}/      - Cancelar aplicación
```

### Favoritos
```
GET    /api/saved-jobs/             - Listar trabajos guardados
POST   /api/saved-jobs/             - Guardar trabajo
DELETE /api/saved-jobs/{id}/        - Quitar de favoritos
```

### Rachas
```
GET    /api/streaks/me/             - Obtener mi racha
POST   /api/streaks/activity/       - Registrar actividad
GET    /api/streaks/activities/     - Listar actividades
GET    /api/streaks/badges/         - Listar insignias ganadas
GET    /api/streaks/leaderboard/    - Tabla de clasificación
```

### Chatbot
```
POST   /api/chatbot/message/        - Enviar mensaje al chatbot
GET    /api/chatbot/history/        - Historial de conversación
POST   /api/chatbot/recommend/      - Obtener recomendaciones de trabajos
```

### Notificaciones
```
POST   /api/notifications/register-device/  - Registrar dispositivo para push
GET    /api/notifications/             - Listar notificaciones
PUT    /api/notifications/{id}/read/   - Marcar como leída
```

## Variables de Entorno (.env)

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=joby_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# JWT
JWT_SECRET_KEY=your-jwt-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# OpenAI (Chatbot)
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4

# Firebase (Push Notifications)
FIREBASE_CREDENTIALS_PATH=/path/to/firebase-credentials.json

# AWS S3 (para archivos)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=joby-files
AWS_S3_REGION_NAME=us-east-1

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## Instalación del Backend

### 1. Crear entorno virtual
```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar base de datos
```bash
# Crear base de datos en PostgreSQL
createdb joby_db

# Ejecutar migraciones
python manage.py makemigrations
python manage.py migrate
```

### 4. Crear superusuario
```bash
python manage.py createsuperuser
```

### 5. Ejecutar servidor
```bash
python manage.py runserver
```

## Docker

### Ejecutar con Docker Compose
```bash
docker-compose up --build
```

Esto levantará:
- Django API en puerto 8000
- PostgreSQL en puerto 5432
- Redis (para caché) en puerto 6379

## Testing

```bash
# Ejecutar todos los tests
python manage.py test

# Con coverage
coverage run --source='.' manage.py test
coverage report
```

## Seguridad

- ✅ Autenticación JWT
- ✅ Passwords hasheados con bcrypt
- ✅ CORS configurado
- ✅ Rate limiting en endpoints
- ✅ Validación de datos con serializers
- ✅ Permisos por rol (IsAuthenticated, IsAdmin, etc.)
- ✅ HTTPS en producción
- ✅ Variables de entorno para secretos

## Próximos Pasos Backend

1. Implementar todos los modelos
2. Crear serializers para cada modelo
3. Implementar vistas y endpoints
4. Configurar autenticación JWT
5. Integrar OpenAI para chatbot
6. Configurar Firebase para push notifications
7. Implementar sistema de recomendaciones con IA
8. Añadir tests unitarios e integración
9. Configurar CI/CD
10. Deploy en AWS/GCP/Azure
