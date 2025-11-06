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
    final response = await _api.get('${ApiConfig.notifications}/');
    final responseData = jsonDecode(response.body);
    
    // Si la respuesta es paginada (tiene 'results'), usa eso
    // Si es un array directo, úsalo como está
    final List<dynamic> data = responseData is Map 
        ? (responseData['results'] ?? [])
        : responseData;
    
    return data.map((json) => AppNotification.fromJson(json)).toList();
  }

  // Obtener notificaciones no leídas
  Future<List<AppNotification>> getUnreadNotifications() async {
    final response = await _api.get(
      '${ApiConfig.notifications}/unread/',
    );
    final responseData = jsonDecode(response.body);
    
    // Manejar respuesta paginada o array directo
    final List<dynamic> data = responseData is Map 
        ? (responseData['results'] ?? [])
        : responseData;
    
    return data.map((json) => AppNotification.fromJson(json)).toList();
  }

  // Marcar como leída
  Future<void> markAsRead(String notificationId) async {
    await _api.post(
      '${ApiConfig.notifications}/$notificationId/mark_as_read/',
    );
  }

  // Marcar todas como leídas
  Future<void> markAllAsRead() async {
    await _api.post(
      '${ApiConfig.notifications}/mark_all_as_read/',
    );
  }

  // Eliminar notificación
  Future<void> deleteNotification(String notificationId) async {
    await _api.delete(
      '${ApiConfig.notifications}/$notificationId/',
    );
  }

  // Obtener cantidad de notificaciones no leídas
  Future<int> getUnreadCount() async {
    final stats = await getStats();
    return stats['unread_count'] ?? 0;
  }

  // Limpiar todas
  Future<void> clearAll() async {
    await _api.post(
      '${ApiConfig.notifications}/clear_all/',
    );
  }

  // Obtener estadísticas
  Future<Map<String, dynamic>> getStats() async {
    final response = await _api.get(
      '${ApiConfig.notifications}/stats/',
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
