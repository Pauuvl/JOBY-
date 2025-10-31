# 🎯 SIGUIENTE PASO: Configurar y Probar el Backend

## ✅ Lo que acabamos de hacer:

1. ✅ **Backend Django completo** con PostgreSQL
2. ✅ **API REST** con autenticación JWT
3. ✅ **Login/Registro** modernizado en Flutter
4. ✅ **Documentación completa** de instalación
5. ✅ **Docker** y scripts de instalación

---

## 🚀 AHORA debes hacer esto:

### **Paso 1: Instalar PostgreSQL** (si no lo tienes)

```powershell
# Descargar e instalar PostgreSQL 14+
# https://www.postgresql.org/download/windows/

# Después de instalar, abrir psql:
psql -U postgres

# Crear la base de datos:
CREATE DATABASE joby_db;
CREATE USER joby_user WITH PASSWORD 'tu_password_seguro';
GRANT ALL PRIVILEGES ON DATABASE joby_db TO joby_user;
\q
```

### **Paso 2: Configurar el Backend**

```powershell
# Navegar al backend
cd backend

# Opción A: Usar script automático (RECOMENDADO)
.\install.ps1

# Opción B: Manual
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# Editar .env con tus credenciales
python manage.py migrate
python manage.py createsuperuser
```

### **Paso 3: Ejecutar el Backend**

```powershell
# Con venv activado:
python manage.py runserver

# Deberías ver:
# Starting development server at http://127.0.0.1:8000/
```

### **Paso 4: Probar la API**

```powershell
# Registrar un usuario de prueba
curl -X POST http://127.0.0.1:8000/api/auth/register/ `
  -H "Content-Type: application/json" `
  -d '{"email":"test@joby.com","name":"Test User","username":"testuser","password":"Test123!","password_confirm":"Test123!"}'

# Login
curl -X POST http://127.0.0.1:8000/api/auth/login/ `
  -H "Content-Type: application/json" `
  -d '{"email":"test@joby.com","password":"Test123!"}'

# Esto te devolverá un access_token que usarás para otras peticiones
```

### **Paso 5: Ver el Admin Panel**

```
1. Abrir navegador
2. Ir a: http://127.0.0.1:8000/admin/
3. Login con el superuser que creaste
4. Podrás gestionar usuarios desde aquí
```

---

## 📝 Archivo .env a configurar

Edita `backend/.env` con estos valores:

```env
# Django
SECRET_KEY=cambia-esto-por-una-clave-secreta-unica
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL  
DB_NAME=joby_db
DB_USER=joby_user
DB_PASSWORD=el_password_que_pusiste
DB_HOST=localhost
DB_PORT=5432

# JWT
JWT_SECRET_KEY=otra-clave-secreta-para-jwt
ACCESS_TOKEN_LIFETIME_MINUTES=60
REFRESH_TOKEN_LIFETIME_DAYS=7

# OpenAI (opcional por ahora, lo usaremos después para el chatbot)
OPENAI_API_KEY=sk-obtener-de-platform.openai.com
OPENAI_MODEL=gpt-4

# Firebase (opcional por ahora, lo usaremos después para notificaciones)
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
```

---

## 🧪 Cómo probar que funciona:

### Test 1: Backend corriendo
```powershell
# Ejecutar
python manage.py runserver

# Ver en navegador
http://127.0.0.1:8000/admin/
```

### Test 2: API de registro
```powershell
# PowerShell
curl -X POST http://127.0.0.1:8000/api/auth/register/ `
  -H "Content-Type: application/json" `
  -d '{"email":"mi@email.com","name":"Mi Nombre","username":"miusuario","password":"MiPass123!","password_confirm":"MiPass123!"}'

# Deberías recibir:
# {
#   "message": "Usuario registrado exitosamente",
#   "user": {...},
#   "tokens": {
#     "access": "eyJ...",
#     "refresh": "eyJ..."
#   }
# }
```

### Test 3: API de login
```powershell
curl -X POST http://127.0.0.1:8000/api/auth/login/ `
  -H "Content-Type: application/json" `
  -d '{"email":"mi@email.com","password":"MiPass123!"}'
```

### Test 4: Obtener perfil
```powershell
# Usa el access_token que recibiste en login o registro
curl -X GET http://127.0.0.1:8000/api/auth/me/ `
  -H "Authorization: Bearer TU_ACCESS_TOKEN_AQUI"
```

---

## 🐛 Problemas comunes:

### Error: "ModuleNotFoundError"
```powershell
# Asegúrate de activar el venv
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Error: "Connection refused" (PostgreSQL)
```powershell
# Verificar que PostgreSQL esté corriendo
Get-Service -Name postgresql*

# Iniciar si está detenido
Start-Service postgresql-x64-14
```

### Error: "role 'joby_user' does not exist"
```sql
-- Conectar a PostgreSQL
psql -U postgres

-- Crear usuario
CREATE USER joby_user WITH PASSWORD 'tu_password';
GRANT ALL PRIVILEGES ON DATABASE joby_db TO joby_user;
```

### Error: "SECRET_KEY not found"
```powershell
# Asegúrate de tener el archivo .env
copy .env.example .env
# Luego edita .env con tus valores
```

---

## 📱 Próximo Paso: Conectar Flutter con Backend

Una vez que el backend esté funcionando:

1. **Instalar dependencia HTTP en Flutter**
   ```yaml
   # En pubspec.yaml, descomentar:
   http: ^1.1.0
   ```

2. **Crear servicio API en Flutter**
   ```dart
   // lib/services/api_service.dart
   class ApiService {
     static const baseUrl = 'http://10.0.2.2:8000/api'; // Android emulator
     // static const baseUrl = 'http://localhost:8000/api'; // iOS simulator
     
     static Future<Map<String, dynamic>> register({
       required String email,
       required String name,
       required String password,
     }) async {
       final response = await http.post(
         Uri.parse('$baseUrl/auth/register/'),
         headers: {'Content-Type': 'application/json'},
         body: jsonEncode({
           'email': email,
           'name': name,
           'username': email.split('@')[0],
           'password': password,
           'password_confirm': password,
         }),
       );
       return jsonDecode(response.body);
     }
   }
   ```

3. **Actualizar LoginScreen para usar API**
   - Descomentar las líneas del TODO en login_screen.dart
   - Reemplazar la simulación con llamadas reales a la API

---

## 🎯 ¿Qué falta implementar?

### Backend (3-4 días)
- [ ] App `jobs` - Gestión de trabajos
- [ ] App `applications` - Aplicaciones a trabajos
- [ ] App `streaks` - Sistema de rachas/gamificación
- [ ] App `chatbot` - Chatbot con OpenAI
- [ ] App `notifications` - Push notifications con Firebase

### Integración (2 días)
- [ ] Conectar Flutter con API Django
- [ ] Manejo de tokens JWT en Flutter
- [ ] Sincronización de datos
- [ ] Caché local

### Funcionalidades Avanzadas (2-3 días)
- [ ] Chatbot funcional con recomendaciones IA
- [ ] Push notifications programadas
- [ ] Sistema de favoritos
- [ ] Búsqueda avanzada
- [ ] Filtros y ordenamiento

---

## 📊 Estado Actual:

```
Progreso Total: ████████░░░░░░░░░░░░ 40%

✅ Frontend Flutter: ████████████████████ 100%
✅ Backend Django: ████████░░░░░░░░░░░░ 40%
⬜ Integración: ░░░░░░░░░░░░░░░░░░░░ 0%
⬜ Chatbot IA: ░░░░░░░░░░░░░░░░░░░░ 0%
⬜ Push Notifications: ░░░░░░░░░░░░░░░░░░░░ 0%
```

---

## 💡 Recomendación:

**¡Empieza configurando el backend AHORA!**

1. Instala PostgreSQL
2. Ejecuta `.\backend\install.ps1`
3. Prueba la API con los comandos curl arriba
4. Una vez funcionando, avísame y continuamos con las apps restantes

**¿Necesitas ayuda con algo específico? ¡Pregúntame! 🚀**

---

**Archivos clave para revisar:**
- `backend/README.md` - Guía completa del backend
- `IMPLEMENTATION_STATUS.md` - Estado del proyecto
- `backend/.env.example` - Variables a configurar
- `backend/apps/users/views.py` - Endpoints implementados
