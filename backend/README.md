# 🚀 Backend Joby - Django REST API

## Instalación Rápida

### 1. Requisitos Previos
- Python 3.10 o superior
- PostgreSQL 14 o superior
- Redis (para Celery)

### 2. Crear Base de Datos PostgreSQL

```bash
# En PowerShell como administrador
# Instalar PostgreSQL si no lo tienes

# Crear base de datos
psql -U postgres
CREATE DATABASE joby_db;
CREATE USER joby_user WITH PASSWORD 'tu_password_seguro';
GRANT ALL PRIVILEGES ON DATABASE joby_db TO joby_user;
\q
```

### 3. Configurar Entorno Virtual

```powershell
# Navegar al backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Si tienes error de ejecución de scripts:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Instalar Dependencias

```powershell
# Instalar todas las dependencias
pip install -r requirements.txt
```

### 5. Configurar Variables de Entorno

```powershell
# Copiar .env.example a .env
copy .env.example .env

# Editar .env con tus credenciales
notepad .env
```

**Variables importantes a configurar:**
```env
SECRET_KEY=genera-una-clave-secreta-unica-aqui
DEBUG=True
DB_NAME=joby_db
DB_USER=joby_user
DB_PASSWORD=tu_password_seguro
DB_HOST=localhost
DB_PORT=5432

# OpenAI API Key (obtener en https://platform.openai.com/api-keys)
OPENAI_API_KEY=sk-tu-api-key-aqui

# Firebase (opcional para push notifications)
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
```

### 6. Ejecutar Migraciones

```powershell
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

### 7. Cargar Datos de Prueba (Opcional)

```powershell
# Crear archivo para cargar trabajos de ejemplo
python manage.py shell

# En el shell de Django:
from apps.jobs.models import Job
from apps.users.models import User
from datetime import datetime, timedelta

# Crear trabajos de ejemplo
Job.objects.create(
    title='Desarrollador Flutter Senior',
    company='TechCorp',
    location='Remoto',
    salary='$80,000 - $100,000',
    description='Buscamos un desarrollador Flutter experimentado...',
    requirements='5+ años de experiencia en Flutter/Dart',
    benefits='Seguro médico, trabajo remoto, bonos',
    type='remote',
    status='open',
    posted_date=datetime.now(),
    expiry_date=datetime.now() + timedelta(days=30)
)

exit()
```

### 8. Ejecutar Servidor

```powershell
# Servidor de desarrollo
python manage.py runserver

# El servidor estará disponible en: http://127.0.0.1:8000
```

### 9. Ejecutar Celery (Para notificaciones programadas)

```powershell
# En una nueva terminal (con venv activado)
celery -A joby_api worker -l info

# En otra terminal para Celery Beat (tareas programadas)
celery -A joby_api beat -l info
```

## 📡 Endpoints API Disponibles

### Autenticación
```
POST   /api/auth/register/              - Registrar usuario
POST   /api/auth/login/                 - Login
POST   /api/auth/logout/                - Logout
POST   /api/auth/token/refresh/         - Refrescar token
GET    /api/auth/me/                    - Usuario actual
PUT    /api/auth/profile/update/        - Actualizar perfil
POST   /api/auth/change-password/       - Cambiar contraseña
POST   /api/auth/register-fcm-token/    - Registrar token FCM
```

### Trabajos
```
GET    /api/jobs/                       - Listar trabajos
POST   /api/jobs/                       - Crear trabajo
GET    /api/jobs/{id}/                  - Detalle de trabajo
PUT    /api/jobs/{id}/                  - Actualizar trabajo
DELETE /api/jobs/{id}/                  - Eliminar trabajo
GET    /api/jobs/search/?q=flutter      - Buscar trabajos
GET    /api/jobs/recommended/           - Recomendaciones con IA
```

### Aplicaciones
```
GET    /api/applications/               - Mis aplicaciones
POST   /api/applications/               - Aplicar a trabajo
GET    /api/applications/{id}/          - Detalle aplicación
PUT    /api/applications/{id}/          - Actualizar estado
DELETE /api/applications/{id}/          - Cancelar aplicación
```

### Rachas/Gamificación
```
GET    /api/streaks/me/                 - Mi racha actual
POST   /api/streaks/activity/           - Registrar actividad
GET    /api/streaks/activities/         - Historial actividades
GET    /api/streaks/badges/             - Mis insignias
GET    /api/streaks/leaderboard/        - Tabla de clasificación
```

### Chatbot IA
```
POST   /api/chatbot/message/            - Enviar mensaje al chatbot
GET    /api/chatbot/history/            - Historial conversación
POST   /api/chatbot/recommend/          - Recomendaciones personalizadas
POST   /api/chatbot/analyze-profile/    - Analizar perfil del usuario
```

### Notificaciones
```
POST   /api/notifications/send/         - Enviar notificación push
GET    /api/notifications/              - Listar notificaciones
PUT    /api/notifications/{id}/read/    - Marcar como leída
GET    /api/notifications/unread-count/ - Contador no leídas
```

## 🧪 Probar la API

### Con cURL
```powershell
# Registrar usuario
curl -X POST http://127.0.0.1:8000/api/auth/register/ `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"test@joby.com\",\"name\":\"Test User\",\"username\":\"testuser\",\"password\":\"TestPassword123!\",\"password_confirm\":\"TestPassword123!\"}'

# Login
curl -X POST http://127.0.0.1:8000/api/auth/login/ `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"test@joby.com\",\"password\":\"TestPassword123!\"}'

# Obtener perfil (usar el access token del login)
curl -X GET http://127.0.0.1:8000/api/auth/me/ `
  -H "Authorization: Bearer tu_access_token_aqui"
```

### Con Postman
1. Importar colección desde: `postman/joby_api.postman_collection.json`
2. Configurar environment con `BASE_URL=http://127.0.0.1:8000`
3. Probar todos los endpoints

## 🔧 Admin Panel

Accede al panel de administración de Django:
```
URL: http://127.0.0.1:8000/admin/
Usuario: (el superuser que creaste)
```

Desde aquí puedes:
- Gestionar usuarios
- Crear/editar trabajos
- Ver aplicaciones
- Administrar rachas e insignias
- Ver logs de chatbot

## 🐛 Troubleshooting

### Error: "role 'joby_user' does not exist"
```sql
-- En psql
CREATE USER joby_user WITH PASSWORD 'tu_password';
GRANT ALL PRIVILEGES ON DATABASE joby_db TO joby_user;
```

### Error: "ModuleNotFoundError"
```powershell
# Asegúrate de tener el venv activado
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Error: "Connection refused" (PostgreSQL)
```powershell
# Verificar que PostgreSQL esté corriendo
Get-Service -Name postgresql*

# Iniciar servicio si está detenido
Start-Service postgresql-x64-14
```

### Error: "Celery no conecta a Redis"
```powershell
# Instalar Redis en Windows
# Opción 1: WSL
wsl
sudo apt-get install redis-server
redis-server

# Opción 2: Docker
docker run -d -p 6379:6379 redis:alpine
```

## 📚 Próximos Pasos

1. ✅ Configurar OpenAI API key para chatbot
2. ✅ Configurar Firebase para push notifications
3. ✅ Conectar Flutter con este backend
4. ✅ Probar flujo completo de registro/login
5. ✅ Implementar recomendaciones con IA

## 🔐 Seguridad en Producción

Antes de deploy a producción:
- [ ] Cambiar `DEBUG=False`
- [ ] Generar nuevo `SECRET_KEY` único
- [ ] Configurar `ALLOWED_HOSTS` correctamente
- [ ] Usar HTTPS
- [ ] Configurar CORS adecuadamente
- [ ] Usar variables de entorno seguras
- [ ] Configurar rate limiting
- [ ] Habilitar logging y monitoring

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs: `python manage.py runserver` mostrará errores
2. Verifica las migraciones: `python manage.py showmigrations`
3. Revisa la consola de PostgreSQL
4. Consulta la documentación de Django REST Framework

---

**¡Backend listo para integrar con Flutter! 🚀**
