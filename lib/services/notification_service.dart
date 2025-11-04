import 'dart:convert';
import '../models/notification.dart';
import '../config/api_config.dart';
import 'api_service.dart';

class NotificationService {
  static final NotificationService _instance = NotificationService._internal();
  factory NotificationService() => _instance;
  NotificationService._internal();

  final ApiService _api = ApiService();

  // Obtener todas las notificaciones
  Future<List<AppNotification>> getNotifications() async {
    final response = await _api.get('${ApiConfig.notifications}/notifications/');
    final List<dynamic> data = jsonDecode(response.body);
    return data.map((json) => AppNotification.fromJson(json)).toList();
  }

  // Obtener notificaciones no leídas
  Future<List<AppNotification>> getUnreadNotifications() async {
    final response = await _api.get(
      '${ApiConfig.notifications}/notifications/unread/',
    );
    final List<dynamic> data = jsonDecode(response.body);
    return data.map((json) => AppNotification.fromJson(json)).toList();
  }

  // Marcar como leída
  Future<void> markAsRead(String notificationId) async {
    await _api.post(
      '${ApiConfig.notifications}/notifications/$notificationId/mark_as_read/',
    );
  }

  // Marcar todas como leídas
  Future<void> markAllAsRead() async {
    await _api.post(
      '${ApiConfig.notifications}/notifications/mark_all_as_read/',
    );
  }

  // Limpiar todas
  Future<void> clearAll() async {
    await _api.post(
      '${ApiConfig.notifications}/notifications/clear_all/',
    );
  }

  // Obtener estadísticas
  Future<Map<String, dynamic>> getStats() async {
    final response = await _api.get(
      '${ApiConfig.notifications}/notifications/stats/',
    );
    return jsonDecode(response.body);
  }

  // Obtener preferencias
  Future<NotificationPreference> getPreferences() async {
    final response = await _api.get(
      '${ApiConfig.notifications}/notification-preferences/me/',
    );
    return NotificationPreference.fromJson(jsonDecode(response.body));
  }

  // Actualizar preferencias
  Future<NotificationPreference> updatePreferences(
    Map<String, dynamic> preferences,
  ) async {
    final response = await _api.patch(
      '${ApiConfig.notifications}/notification-preferences/me/',
      body: preferences,
    );
    return NotificationPreference.fromJson(jsonDecode(response.body));
  }

  // Registrar token de notificaciones push
  Future<void> registerPushToken(String token, String deviceType) async {
    await _api.post(
      '${ApiConfig.notifications}/push-tokens/',
      body: {
        'token': token,
        'device_type': deviceType,
      },
    );
  }
}
