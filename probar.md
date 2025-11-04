# 1. Probar manualmente el envío de recordatorios:
python manage.py send_streak_reminders

# 2. Ver las notificaciones del usuario (desde Flutter):
GET /api/notifications/
GET /api/notifications/unread/

# 3. Marcar notificación como leída:
POST /api/notifications/{id}/mark_as_read/