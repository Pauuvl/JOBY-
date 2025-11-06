# 🎯 Guía de Demostración: Sistema de Alertas de Trabajo

## 📋 Resumen
Este sistema permite recibir notificaciones personalizadas sobre vacantes que coincidan con el perfil del usuario.

## 🚀 Pasos para la Demostración

### 1️⃣ Iniciar el Backend (Terminal 1)

```powershell
cd backend
python manage.py runserver 0.0.0.0:8000
```

Verifica que el servidor esté corriendo en `http://localhost:8000`

### 2️⃣ Generar Alertas de Prueba (Terminal 2)

El sistema incluye un comando especial para demostración:

```powershell
cd backend

# Opción 1: Crear trabajos de muestra y enviar alerta a un usuario específico
python manage.py send_job_alerts --email usuario@ejemplo.com --create-jobs

# Opción 2: Enviar alertas a todos los usuarios activos
python manage.py send_job_alerts --all --create-jobs

# Opción 3: Solo enviar alertas sin crear nuevos trabajos
python manage.py send_job_alerts --email usuario@ejemplo.com
```

**💡 Tip:** Usa el email del usuario que creaste durante el registro.

### 3️⃣ Ejecutar la Aplicación Flutter (Terminal 3)

```powershell
# Para navegador web (recomendado para demo)
flutter run -d chrome

# O para Android emulator
flutter run
```

### 4️⃣ Ver las Notificaciones en la App

1. **Inicia sesión** con tu usuario
2. En la pantalla principal (Home), busca el **ícono de campana 🔔** en la esquina superior derecha
3. **Toca el ícono** para ver todas las notificaciones
4. Las notificaciones mostrarán:
   - 💼 Ícono de trabajo
   - **Título**: "Nuevas vacantes disponibles"
   - **Lista de trabajos** con porcentaje de coincidencia
   - **Badges** en notificaciones no leídas

### 5️⃣ Interactuar con las Notificaciones

- **Toca una notificación** para marcarla como leída
- **Desliza a la izquierda** para eliminar una notificación
- **Marca todas como leídas** usando el botón en el menú superior
- **Actualiza la lista** deslizando hacia abajo (pull to refresh)

## 🎨 Trabajos de Ejemplo que se Crean

El comando `--create-jobs` genera 5 vacantes de muestra:

1. **Desarrollador Python Senior**
   - Skills: Python, Django, PostgreSQL, Docker, AWS
   - Salario: $80,000 - $120,000
   - Ubicación: Madrid, España

2. **Frontend Developer React**
   - Skills: React, JavaScript, TypeScript, CSS, Git
   - Salario: $50,000 - $75,000
   - Ubicación: Barcelona, España

3. **Full Stack Developer**
   - Skills: JavaScript, Node.js, React, MongoDB, Express
   - Salario: $60,000 - $90,000
   - Ubicación: Valencia, España

4. **Data Scientist**
   - Skills: Python, Machine Learning, TensorFlow, Pandas, SQL
   - Salario: $90,000 - $130,000
   - Ubicación: Madrid, España

5. **Mobile Developer Flutter**
   - Skills: Flutter, Dart, Firebase, Git, REST APIs
   - Salario: $55,000 - $85,000
   - Ubicación: Remoto

## 🔍 Cómo Funciona el Matching

El sistema calcula un **porcentaje de coincidencia** basado en:

- **40% - Habilidades**: Compara las skills del usuario con los requisitos del trabajo
- **30% - Ubicación**: Considera si el trabajo es remoto o coincide con la ubicación del usuario
- **30% - Experiencia**: Analiza el nivel de experiencia requerido

Solo se envían alertas para trabajos con **60% o más de coincidencia**.

## ⚙️ Personalización de Alertas

Los usuarios pueden configurar sus preferencias de alertas en:
- Frecuencia: Inmediata, Diaria, Semanal
- Criterios de matching: Skills, Ubicación, Experiencia
- Filtros: Tipos de trabajo, ubicaciones preferidas, solo remoto
- Salario mínimo deseado

**Nota:** La UI para gestionar estas preferencias está pendiente de implementación. Actualmente se pueden modificar desde el panel de administración de Django:

```
http://localhost:8000/admin/users/jobalertpreference/
```

## 🎤 Puntos Clave para la Presentación

1. **Relevancia**: "El sistema solo muestra trabajos relevantes para el usuario"
2. **Scoring**: "Cada trabajo tiene un porcentaje de coincidencia"
3. **Personalización**: "El usuario puede ajustar qué tipo de alertas quiere recibir"
4. **Tiempo Real**: "Las notificaciones aparecen al crear nuevas vacantes"
5. **UX Amigable**: "Interfaz intuitiva con acciones de swipe y tap"

## 🐛 Troubleshooting

### El comando no encuentra al usuario
```powershell
# Verifica que el usuario existe
python manage.py shell
>>> from apps.users.models import User
>>> User.objects.filter(email='tu@email.com').exists()
```

### No aparecen notificaciones
1. Verifica que el backend esté corriendo
2. Refresca la lista (pull to refresh)
3. Revisa la consola del backend para errores
4. Verifica que el usuario tenga `is_active=True`

### Error de CORS en el navegador
- Ya está configurado para desarrollo
- Verifica que `CORS_ALLOW_ALL_ORIGINS = True` en `settings.py`

## 📊 Endpoints de la API

Para desarrolladores que quieran explorar:

- `GET /api/auth/job-alerts/` - Ver preferencias de alertas
- `PUT /api/auth/job-alerts/` - Actualizar preferencias
- `GET /api/auth/matching-jobs/` - Ver trabajos que coinciden
- `POST /api/auth/check-alerts/` - Verificar nuevas alertas
- `GET /api/notifications/notifications/` - Lista de notificaciones
- `POST /api/notifications/notifications/{id}/mark_as_read/` - Marcar como leída

## ✅ Checklist de Demo

- [ ] Backend corriendo en puerto 8000
- [ ] Usuario registrado y con skills configuradas
- [ ] Comando ejecutado exitosamente
- [ ] Flutter app corriendo
- [ ] Usuario logueado
- [ ] Notificaciones visibles en el ícono de campana
- [ ] Demostración de interacciones (tap, swipe, refresh)

---

**¡Buena suerte con tu presentación! 🚀**
