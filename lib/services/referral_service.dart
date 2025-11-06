import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../config/api_config.dart';
import '../models/referral.dart';

class ReferralService {
  final _storage = const FlutterSecureStorage();

  Future<Map<String, String>> _getHeaders() async {
    final token = await _storage.read(key: 'access_token');
    return {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer $token',
    };
  }

  /// Get user's referral code
  Future<ReferralCode> getMyCode() async {
    try {
      final headers = await _getHeaders();
      final response = await http.get(
        Uri.parse('${ApiConfig.baseUrl}/auth/referral/my_code/'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        return ReferralCode.fromJson(json.decode(response.body));
      } else {
        throw Exception('Error al obtener código de referido: ${response.statusCode}');
      }
    } catch (e) {
      print('Error getting referral code: $e');
      rethrow;
    }
  }

  /// Get user's referrals
  Future<List<Referral>> getMyReferrals() async {
    try {
      final headers = await _getHeaders();
      final response = await http.get(
        Uri.parse('${ApiConfig.baseUrl}/auth/referral/my_referrals/'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.map((item) => Referral.fromJson(item)).toList();
      } else {
        throw Exception('Error al obtener referidos: ${response.statusCode}');
      }
    } catch (e) {
      print('Error getting referrals: $e');
      rethrow;
    }
  }

  /// Get referral statistics
  Future<ReferralStats> getStats() async {
    try {
      final headers = await _getHeaders();
      final response = await http.get(
        Uri.parse('${ApiConfig.baseUrl}/auth/referral/stats/'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        return ReferralStats.fromJson(json.decode(response.body));
      } else {
        throw Exception('Error al obtener estadísticas: ${response.statusCode}');
      }
    } catch (e) {
      print('Error getting stats: $e');
      rethrow;
    }
  }

  /// Get leaderboard
  Future<List<LeaderboardEntry>> getLeaderboard({int limit = 10}) async {
    try {
      final headers = await _getHeaders();
      final response = await http.get(
        Uri.parse('${ApiConfig.baseUrl}/auth/referral/leaderboard/?limit=$limit'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.map((item) => LeaderboardEntry.fromJson(item)).toList();
      } else {
        throw Exception('Error al obtener ranking: ${response.statusCode}');
      }
    } catch (e) {
      print('Error getting leaderboard: $e');
      rethrow;
    }
  }

  /// Get points balance
  Future<int> getPointsBalance() async {
    try {
      final headers = await _getHeaders();
      final response = await http.get(
        Uri.parse('${ApiConfig.baseUrl}/auth/points/balance/'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data['points'];
      } else {
        throw Exception('Error al obtener puntos: ${response.statusCode}');
      }
    } catch (e) {
      print('Error getting points balance: $e');
      rethrow;
    }
  }

  /// Get points history
  Future<List<PointsTransaction>> getPointsHistory({int limit = 50}) async {
    try {
      final headers = await _getHeaders();
      final response = await http.get(
        Uri.parse('${ApiConfig.baseUrl}/auth/points/history/?limit=$limit'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.map((item) => PointsTransaction.fromJson(item)).toList();
      } else {
        throw Exception('Error al obtener historial: ${response.statusCode}');
      }
    } catch (e) {
      print('Error getting points history: $e');
      rethrow;
    }
  }

  /// Get available rewards
  Future<List<Reward>> getRewards() async {
    try {
      final headers = await _getHeaders();
      final response = await http.get(
        Uri.parse('${ApiConfig.baseUrl}/auth/points/rewards/'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.map((item) => Reward.fromJson(item)).toList();
      } else {
        throw Exception('Error al obtener recompensas: ${response.statusCode}');
      }
    } catch (e) {
      print('Error getting rewards: $e');
      rethrow;
    }
  }

  /// Redeem a reward
  Future<RewardRedemption> redeemReward(int rewardId) async {
    try {
      final headers = await _getHeaders();
      final response = await http.post(
        Uri.parse('${ApiConfig.baseUrl}/auth/points/redeem/'),
        headers: headers,
        body: json.encode({'reward_id': rewardId}),
      );

      if (response.statusCode == 201) {
        return RewardRedemption.fromJson(json.decode(response.body));
      } else {
        final error = json.decode(response.body);
        throw Exception(error['error'] ?? 'Error al canjear recompensa');
      }
    } catch (e) {
      print('Error redeeming reward: $e');
      rethrow;
    }
  }

  /// Get user's redemptions
  Future<List<RewardRedemption>> getMyRedemptions() async {
    try {
      final headers = await _getHeaders();
      final response = await http.get(
        Uri.parse('${ApiConfig.baseUrl}/auth/points/my_redemptions/'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.map((item) => RewardRedemption.fromJson(item)).toList();
      } else {
        throw Exception('Error al obtener canjes: ${response.statusCode}');
      }
    } catch (e) {
      print('Error getting redemptions: $e');
      rethrow;
    }
  }
}
