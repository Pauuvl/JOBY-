import 'dart:convert';
import '../models/challenge.dart';
import '../config/api_config.dart';
import 'api_service.dart';

class ChallengeService {
  static final ChallengeService _instance = ChallengeService._internal();
  factory ChallengeService() => _instance;
  ChallengeService._internal();

  final ApiService _api = ApiService();

  // Obtener retos activos
  Future<List<UserChallenge>> getActiveChallenges() async {
    final response = await _api.get('${ApiConfig.streaks}/user-challenges/active/');
    final responseData = jsonDecode(response.body);
    
    final List<dynamic> data = responseData is Map 
        ? (responseData['results'] ?? [])
        : responseData;
    
    return data.map((json) => UserChallenge.fromJson(json)).toList();
  }

  // Obtener retos completados
  Future<List<UserChallenge>> getCompletedChallenges() async {
    final response = await _api.get('${ApiConfig.streaks}/user-challenges/completed/');
    final responseData = jsonDecode(response.body);
    
    final List<dynamic> data = responseData is Map 
        ? (responseData['results'] ?? [])
        : responseData;
    
    return data.map((json) => UserChallenge.fromJson(json)).toList();
  }

  // Obtener retos disponibles
  Future<List<Challenge>> getAvailableChallenges() async {
    final response = await _api.get('${ApiConfig.streaks}/challenges/available/');
    final responseData = jsonDecode(response.body);
    
    final List<dynamic> data = responseData is Map 
        ? (responseData['results'] ?? [])
        : responseData;
    
    return data.map((json) => Challenge.fromJson(json)).toList();
  }

  // Actualizar progreso de un reto
  Future<UserChallenge> updateProgress(String challengeId, int increment) async {
    final response = await _api.post(
      '${ApiConfig.streaks}/user-challenges/update_progress/',
      body: {
        'challenge_id': challengeId,
        'increment': increment,
      },
    );
    return UserChallenge.fromJson(jsonDecode(response.body));
  }

  // Iniciar un reto
  Future<UserChallenge> startChallenge(String challengeId) async {
    final response = await _api.post(
      '${ApiConfig.streaks}/user-challenges/start/',
      body: {
        'challenge_id': challengeId,
      },
    );
    return UserChallenge.fromJson(jsonDecode(response.body));
  }

  // Obtener estadísticas de retos
  Future<Map<String, dynamic>> getChallengeStats() async {
    final response = await _api.get('${ApiConfig.streaks}/user-challenges/stats/');
    return jsonDecode(response.body);
  }
}
