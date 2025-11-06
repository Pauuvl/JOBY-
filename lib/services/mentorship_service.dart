import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../config/api_config.dart';
import '../models/mentorship.dart';

class MentorshipService {
  final storage = const FlutterSecureStorage();

  Future<String?> _getToken() async {
    return await storage.read(key: 'access_token');
  }

  Future<Map<String, String>> _getHeaders() async {
    final token = await _getToken();
    return {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer $token',
    };
  }

  /// Find potential mentors based on profile similarity
  Future<List<ProfileMatch>> findMentors() async {
    try {
      final headers = await _getHeaders();
      final response = await http.get(
        Uri.parse('${ApiConfig.baseUrl}/auth/mentorship/find_mentors/'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(utf8.decode(response.bodyBytes));
        return data.map((json) => ProfileMatch.fromJson(json)).toList();
      } else {
        throw Exception('Error al cargar mentores: ${response.statusCode}');
      }
    } catch (e) {
      print('Error finding mentors: $e');
      throw Exception('Error al buscar mentores');
    }
  }

  /// Send mentorship request to a mentor
  Future<MentorshipRequest> sendRequest({
    required String toUserId,
    required String message,
  }) async {
    try {
      final headers = await _getHeaders();
      final response = await http.post(
        Uri.parse('${ApiConfig.baseUrl}/auth/mentorship/send_request/'),
        headers: headers,
        body: json.encode({
          'to_user_id': toUserId,
          'message': message,
        }),
      );

      if (response.statusCode == 201) {
        final data = json.decode(utf8.decode(response.bodyBytes));
        return MentorshipRequest.fromJson(data);
      } else {
        final error = json.decode(utf8.decode(response.bodyBytes));
        throw Exception(error['error'] ?? 'Error al enviar solicitud');
      }
    } catch (e) {
      print('Error sending request: $e');
      rethrow;
    }
  }

  /// Get user's mentorship requests
  Future<List<MentorshipRequest>> getMyRequests({String type = 'all'}) async {
    try {
      final headers = await _getHeaders();
      final response = await http.get(
        Uri.parse('${ApiConfig.baseUrl}/auth/mentorship/my_requests/?type=$type'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(utf8.decode(response.bodyBytes));
        return data.map((json) => MentorshipRequest.fromJson(json)).toList();
      } else {
        throw Exception('Error al cargar solicitudes');
      }
    } catch (e) {
      print('Error getting requests: $e');
      throw Exception('Error al cargar solicitudes');
    }
  }

  /// Respond to a mentorship request (accept or decline)
  Future<MentorshipRequest> respondToRequest({
    required int requestId,
    required String action, // 'accept' or 'decline'
    String? responseMessage,
  }) async {
    try {
      final headers = await _getHeaders();
      final response = await http.post(
        Uri.parse('${ApiConfig.baseUrl}/auth/mentorship/$requestId/respond/'),
        headers: headers,
        body: json.encode({
          'action': action,
          'response_message': responseMessage ?? '',
        }),
      );

      if (response.statusCode == 200) {
        final data = json.decode(utf8.decode(response.bodyBytes));
        return MentorshipRequest.fromJson(data);
      } else {
        final error = json.decode(utf8.decode(response.bodyBytes));
        throw Exception(error['error'] ?? 'Error al responder');
      }
    } catch (e) {
      print('Error responding to request: $e');
      rethrow;
    }
  }

  /// Cancel a sent mentorship request
  Future<MentorshipRequest> cancelRequest(int requestId) async {
    try {
      final headers = await _getHeaders();
      final response = await http.post(
        Uri.parse('${ApiConfig.baseUrl}/auth/mentorship/$requestId/cancel/'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        final data = json.decode(utf8.decode(response.bodyBytes));
        return MentorshipRequest.fromJson(data);
      } else {
        throw Exception('Error al cancelar solicitud');
      }
    } catch (e) {
      print('Error canceling request: $e');
      throw Exception('Error al cancelar solicitud');
    }
  }
}
