import 'dart:convert';
import '../models/streak.dart';
import '../config/api_config.dart';
import 'api_service.dart';

class StreakService {
  static final StreakService _instance = StreakService._internal();
  factory StreakService() => _instance;
  StreakService._internal();

  final ApiService _api = ApiService();

  // Obtener mi racha
  Future<Streak> getMyStreak() async {
    final response = await _api.get('${ApiConfig.streaks}/streaks/my_streak/');
    return Streak.fromJson(jsonDecode(response.body));
  }

  // Registrar actividad diaria (gana +5 puntos)
  Future<Streak> recordActivity() async {
    final response = await _api.post(
      '${ApiConfig.streaks}/streaks/record_activity/',
    );
    final data = jsonDecode(response.body);
    // El backend devuelve {streak: {...}, streak_updated: bool, message: string}
    return Streak.fromJson(data['streak']);
  }

  // Obtener todos los logros
  Future<List<Achievement>> getAllAchievements() async {
    final response = await _api.get('${ApiConfig.streaks}/achievements/');
    final List<dynamic> data = jsonDecode(response.body);
    return data.map((json) => Achievement.fromJson(json)).toList();
  }

  // Obtener mis logros
  Future<List<Achievement>> getMyAchievements() async {
    try {
      final response = await _api.get(
        '${ApiConfig.streaks}/achievements/my_achievements/',
      );
      final dynamic responseData = jsonDecode(response.body);
      
      // Si es lista vacía, retornar lista vacía
      if (responseData is List && responseData.isEmpty) {
        return [];
      }
      
      // Si es lista con datos, procesar cada elemento
      if (responseData is List) {
        return responseData.map<Achievement>((item) {
          // El backend devuelve {id, user, achievement, achievement_details, earned_at}
          // Necesitamos extraer achievement_details
          final achievementData = item['achievement_details'] ?? item;
          return Achievement.fromJson(achievementData);
        }).toList();
      }
      
      return [];
    } catch (e) {
      print('Error en getMyAchievements: $e');
      return [];
    }
  }

  // Obtener logros disponibles
  Future<List<Achievement>> getAvailableAchievements() async {
    final response = await _api.get(
      '${ApiConfig.streaks}/achievements/available/',
    );
    final List<dynamic> data = jsonDecode(response.body);
    return data.map((json) => Achievement.fromJson(json)).toList();
  }

  // Verificar progreso de logros
  Future<void> checkAchievementProgress() async {
    await _api.post('${ApiConfig.streaks}/achievements/check_progress/');
  }

  // Obtener historial de puntos
  Future<List<PointsHistory>> getPointsHistory() async {
    try {
      final response = await _api.get('${ApiConfig.streaks}/points-history/');
      final dynamic responseData = jsonDecode(response.body);
      
      // Si es un mapa (probablemente sin datos), retornar lista vacía
      if (responseData is Map) {
        return [];
      }
      
      // Si es lista, procesar normalmente
      if (responseData is List) {
        return responseData.map((json) => PointsHistory.fromJson(json)).toList();
      }
      
      return [];
    } catch (e) {
      print('Error en getPointsHistory: $e');
      return [];
    }
  }

  // Obtener resumen de puntos
  Future<Map<String, dynamic>> getPointsSummary() async {
    final response = await _api.get(
      '${ApiConfig.streaks}/points-history/summary/',
    );
    return jsonDecode(response.body);
  }

  // Obtener tabla de clasificación
  Future<List<LeaderboardEntry>> getLeaderboard({
    String period = 'all_time',
  }) async {
    final response = await _api.get(
      '${ApiConfig.streaks}/leaderboard/top_users/',
      queryParams: {'period': period},
    );
    final List<dynamic> data = jsonDecode(response.body);
    return data.map((json) => LeaderboardEntry.fromJson(json)).toList();
  }

  // Obtener mi posición en la tabla
  Future<Map<String, dynamic>> getMyRank({String period = 'all_time'}) async {
    final response = await _api.get(
      '${ApiConfig.streaks}/leaderboard/my_rank/',
      queryParams: {'period': period},
    );
    return jsonDecode(response.body);
  }

  // Obtener estadísticas completas
  Future<Map<String, dynamic>> getMyStats() async {
    final response = await _api.get('${ApiConfig.streaks}/stats/me/');
    return jsonDecode(response.body);
  }
}
