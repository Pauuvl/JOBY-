# 🔔 Sistema de Notificaciones Push - Joby

## Descripción

Sistema de notificaciones push para mantener a los usuarios comprometidos con la app, recordarles mantener sus rachas y alertarles sobre nuevos trabajos relevantes.

## Tipos de Notificaciones

### 1. Rachas (Streaks)
- **Recordatorio Diario**: "¡No pierdas tu racha de X días! 🔥"
- **Racha en Peligro**: "Solo quedan 3 horas para mantener tu racha"
- **Nueva Insignia**: "¡Felicidades! Ganaste la insignia: 🏆"
- **Récord Personal**: "¡Nuevo récord! X días consecutivos"

### 2. Trabajos
- **Nuevo Trabajo Compatible**: "Nuevo trabajo perfecto para ti: {title}"
- **Trabajo Guardado**: "El trabajo guardado '{title}' cierra pronto"
- **Respuesta a Aplicación**: "Tu aplicación a {title} fue revisada"
- **Recomendación Semanal**: "5 nuevos trabajos que podrían interesarte"

### 3. Chatbot
- **Mensaje del Asistente**: "Tu asistente tiene nuevas recomendaciones"
- **Recordatorio de Chat**: "¿Necesitas ayuda buscando trabajo?"

### 4. Perfil
- **Completar Perfil**: "Completa tu perfil para mejores recomendaciones"
- **Actualización Sugerida**: "Actualiza tu perfil con nuevas habilidades"

## Implementación con Firebase

### 1. Configuración Firebase

#### Crear Proyecto Firebase
1. Ve a https://console.firebase.google.com/
2. Crea un nuevo proyecto "Joby"
3. Añade una app Android
4. Añade una app iOS
5. Descarga `google-services.json` (Android) y `GoogleService-Info.plist` (iOS)

#### Android Setup
```gradle
// android/build.gradle
buildscript {
    dependencies {
        classpath 'com.google.gms:google-services:4.4.0'
    }
}

// android/app/build.gradle
apply plugin: 'com.google.gms.google-services'

dependencies {
    implementation platform('com.google.firebase:firebase-bom:32.7.0')
    implementation 'com.google.firebase:firebase-messaging'
}
```

Coloca `google-services.json` en `android/app/`

#### iOS Setup
```ruby
# ios/Podfile
pod 'Firebase/Messaging'
```

Coloca `GoogleService-Info.plist` en `ios/Runner/`

### 2. Flutter Dependencies

```yaml
# pubspec.yaml
dependencies:
  firebase_core: ^2.24.2
  firebase_messaging: ^14.7.9
  flutter_local_notifications: ^16.3.0
```

### 3. Inicialización en Flutter

```dart
// lib/main.dart
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'firebase_options.dart';

// Handler para mensajes en background
@pragma('vm:entry-point')
Future<void> _firebaseMessagingBackgroundHandler(RemoteMessage message) async {
  await Firebase.initializeApp();
  print('Handling background message: ${message.messageId}');
}

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  
  FirebaseMessaging.onBackgroundMessage(_firebaseMessagingBackgroundHandler);
  
  runApp(const JobSearchApp());
}
```

### 4. Servicio de Notificaciones

```dart
// lib/services/notification_service.dart
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';

class NotificationService {
  static final NotificationService _instance = NotificationService._internal();
  factory NotificationService() => _instance;
  NotificationService._internal();

  final FirebaseMessaging _fcm = FirebaseMessaging.instance;
  final FlutterLocalNotificationsPlugin _localNotifications = 
      FlutterLocalNotificationsPlugin();

  Future<void> initialize() async {
    // Solicitar permisos
    NotificationSettings settings = await _fcm.requestPermission(
      alert: true,
      badge: true,
      sound: true,
      announcement: false,
      carPlay: false,
      criticalAlert: false,
      provisional: false,
    );

    if (settings.authorizationStatus == AuthorizationStatus.authorized) {
      print('User granted permission');
    }

    // Configurar notificaciones locales
    const androidSettings = AndroidInitializationSettings('@mipmap/ic_launcher');
    const iosSettings = DarwinInitializationSettings();
    
    const initSettings = InitializationSettings(
      android: androidSettings,
      iOS: iosSettings,
    );

    await _localNotifications.initialize(
      initSettings,
      onDidReceiveNotificationResponse: _onNotificationTap,
    );

    // Obtener FCM token
    String? token = await _fcm.getToken();
    print('FCM Token: $token');
    
    // TODO: Enviar token al backend
    // await ApiService().registerDevice(token);

    // Escuchar mensajes en foreground
    FirebaseMessaging.onMessage.listen(_handleForegroundMessage);
    
    // Manejar tap en notificación
    FirebaseMessaging.onMessageOpenedApp.listen(_handleNotificationTap);
  }

  void _handleForegroundMessage(RemoteMessage message) {
    print('Got a message in foreground!');
    print('Message data: ${message.data}');

    if (message.notification != null) {
      _showLocalNotification(message);
    }
  }

  Future<void> _showLocalNotification(RemoteMessage message) async {
    const androidDetails = AndroidNotificationDetails(
      'joby_channel',
      'Joby Notifications',
      channelDescription: 'Canal para notificaciones de Joby',
      importance: Importance.high,
      priority: Priority.high,
      icon: '@mipmap/ic_launcher',
    );

    const iosDetails = DarwinNotificationDetails();

    const notificationDetails = NotificationDetails(
      android: androidDetails,
      iOS: iosDetails,
    );

    await _localNotifications.show(
      message.hashCode,
      message.notification?.title,
      message.notification?.body,
      notificationDetails,
      payload: message.data.toString(),
    );
  }

  void _handleNotificationTap(RemoteMessage message) {
    print('Notification tapped: ${message.data}');
    
    // Navegar según el tipo de notificación
    final type = message.data['type'];
    switch (type) {
      case 'new_job':
        // Navegar a detalles del trabajo
        final jobId = message.data['job_id'];
        // Navigator.push(...);
        break;
      case 'streak_reminder':
        // Navegar a pantalla de rachas
        // Navigator.push(...);
        break;
      case 'chatbot_message':
        // Navegar a chatbot
        // Navigator.push(...);
        break;
    }
  }

  void _onNotificationTap(NotificationResponse response) {
    print('Local notification tapped: ${response.payload}');
  }

  // Programar notificación local
  Future<void> scheduleStreakReminder({
    required int hour,
    required int minute,
  }) async {
    const androidDetails = AndroidNotificationDetails(
      'streak_reminders',
      'Streak Reminders',
      channelDescription: 'Recordatorios para mantener tu racha',
      importance: Importance.high,
      priority: Priority.high,
    );

    const iosDetails = DarwinNotificationDetails();

    const notificationDetails = NotificationDetails(
      android: androidDetails,
      iOS: iosDetails,
    );

    await _localNotifications.zonedSchedule(
      0,
      '🔥 ¡No pierdas tu racha!',
      'Ingresa a Joby para mantener tu racha activa',
      _nextInstanceOfTime(hour, minute),
      notificationDetails,
      androidScheduleMode: AndroidScheduleMode.exactAllowWhileIdle,
      uiLocalNotificationDateInterpretation:
          UILocalNotificationDateInterpretation.absoluteTime,
      matchDateTimeComponents: DateTimeComponents.time,
    );
  }

  tz.TZDateTime _nextInstanceOfTime(int hour, int minute) {
    final tz.TZDateTime now = tz.TZDateTime.now(tz.local);
    tz.TZDateTime scheduledDate = tz.TZDateTime(
      tz.local,
      now.year,
      now.month,
      now.day,
      hour,
      minute,
    );
    
    if (scheduledDate.isBefore(now)) {
      scheduledDate = scheduledDate.add(const Duration(days: 1));
    }
    
    return scheduledDate;
  }
}
```

### 5. Backend Django - Envío de Notificaciones

```python
# backend/apps/notifications/fcm_service.py
from firebase_admin import messaging
import firebase_admin
from firebase_admin import credentials

# Inicializar Firebase Admin SDK
cred = credentials.Certificate('path/to/serviceAccountKey.json')
firebase_admin.initialize_app(cred)

class FCMService:
    @staticmethod
    def send_to_device(device_token, title, body, data=None):
        """Enviar notificación a un dispositivo específico"""
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data or {},
            token=device_token,
        )
        
        try:
            response = messaging.send(message)
            print(f'Successfully sent message: {response}')
            return True
        except Exception as e:
            print(f'Error sending message: {e}')
            return False
    
    @staticmethod
    def send_to_topic(topic, title, body, data=None):
        """Enviar notificación a un topic (grupo de usuarios)"""
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data or {},
            topic=topic,
        )
        
        try:
            response = messaging.send(message)
            return True
        except Exception as e:
            print(f'Error: {e}')
            return False
    
    @staticmethod
    def send_streak_reminder(user):
        """Enviar recordatorio de racha"""
        if not user.device_token:
            return False
            
        return FCMService.send_to_device(
            device_token=user.device_token,
            title='🔥 ¡No pierdas tu racha!',
            body=f'Llevas {user.streak.current_streak} días. ¡Sigue así!',
            data={
                'type': 'streak_reminder',
                'screen': 'streak',
            }
        )
    
    @staticmethod
    def send_new_job_notification(user, job):
        """Notificar nuevo trabajo compatible"""
        if not user.device_token:
            return False
            
        return FCMService.send_to_device(
            device_token=user.device_token,
            title='Nuevo trabajo para ti',
            body=f'{job.title} en {job.company}',
            data={
                'type': 'new_job',
                'job_id': str(job.id),
                'screen': 'job_detail',
            }
        )
```

```python
# backend/apps/notifications/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import DeviceToken

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_device(request):
    """Registrar token FCM del dispositivo"""
    token = request.data.get('token')
    platform = request.data.get('platform')  # 'android' o 'ios'
    
    if not token:
        return Response({'error': 'Token required'}, status=400)
    
    # Guardar o actualizar token
    DeviceToken.objects.update_or_create(
        user=request.user,
        platform=platform,
        defaults={'token': token}
    )
    
    return Response({'message': 'Device registered successfully'})
```

### 6. Modelos Django

```python
# backend/apps/notifications/models.py
from django.db import models
from apps.users.models import User

class DeviceToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    platform = models.CharField(
        max_length=10,
        choices=[('android', 'Android'), ('ios', 'iOS')]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'platform')

class NotificationLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    type = models.CharField(max_length=50)
    data = models.JSONField(default=dict)
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    success = models.BooleanField(default=True)
```

### 7. Tareas Programadas (Celery)

```python
# backend/apps/notifications/tasks.py
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from apps.users.models import User
from .fcm_service import FCMService

@shared_task
def send_daily_streak_reminders():
    """Enviar recordatorios diarios de racha"""
    # Usuarios que no han tenido actividad hoy
    today = timezone.now().date()
    users = User.objects.filter(
        is_active=True,
        streak__last_activity_date__lt=today
    )
    
    for user in users:
        if user.device_token:
            FCMService.send_streak_reminder(user)

@shared_task
def send_new_jobs_notification():
    """Notificar sobre nuevos trabajos compatibles"""
    from apps.jobs.models import Job
    
    # Trabajos publicados en las últimas 24 horas
    yesterday = timezone.now() - timedelta(days=1)
    new_jobs = Job.objects.filter(
        posted_date__gte=yesterday,
        status='Open'
    )
    
    for job in new_jobs:
        # Encontrar usuarios compatibles
        compatible_users = User.objects.filter(
            is_active=True,
            # Lógica de compatibilidad
        )
        
        for user in compatible_users:
            FCMService.send_new_job_notification(user, job)

# Configurar en settings.py con Celery Beat
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'send-daily-reminders': {
        'task': 'apps.notifications.tasks.send_daily_streak_reminders',
        'schedule': crontab(hour=20, minute=0),  # 8 PM diario
    },
    'send-new-jobs': {
        'task': 'apps.notifications.tasks.send_new_jobs_notification',
        'schedule': crontab(hour='*/6'),  # Cada 6 horas
    },
}
```

## Mejores Prácticas

1. **Personalización**: Notificaciones basadas en preferencias del usuario
2. **Frecuencia**: No más de 3-5 notificaciones al día
3. **Timing**: Enviar en horarios apropiados (9 AM - 9 PM)
4. **Relevancia**: Solo notificar contenido relevante
5. **Opt-out**: Permitir desactivar notificaciones por categoría
6. **Analytics**: Trackear tasa de apertura y engagement

## Testing

```dart
// En development, puedes probar notificaciones así:
ElevatedButton(
  onPressed: () async {
    await NotificationService().scheduleStreakReminder(
      hour: DateTime.now().hour,
      minute: DateTime.now().minute + 1,
    );
  },
  child: Text('Test Notification'),
)
```

## Próximos Pasos

1. Configurar proyecto Firebase
2. Implementar NotificationService en Flutter
3. Crear endpoints en Django
4. Configurar Celery para tareas programadas
5. Implementar lógica de compatibilidad de trabajos
6. Añadir analytics de notificaciones
7. Crear panel de configuración de notificaciones
