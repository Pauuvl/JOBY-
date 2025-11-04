import 'dart:convert';
import '../models/application.dart';
import '../config/api_config.dart';
import 'api_service.dart';

class ApplicationService {
  static final ApplicationService _instance = ApplicationService._internal();
  factory ApplicationService() => _instance;
  ApplicationService._internal();

  final ApiService _api = ApiService();

  // Obtener mis aplicaciones
  Future<List<Application>> getMyApplications({String? status}) async {
    final queryParams = <String, String>{};
    if (status != null) queryParams['status'] = status;

    final response = await _api.get(
      '${ApiConfig.applications}/applications/my_applications/',
      queryParams: queryParams,
    );

    final List<dynamic> data = jsonDecode(response.body);
    return data.map((json) => Application.fromJson(json)).toList();
  }

  // Aplicar a un empleo
  Future<Application> apply({
    required String jobId,
    required String coverLetter,
    String? portfolioUrl,
  }) async {
    final body = {
      'job': jobId,
      'cover_letter': coverLetter,
      if (portfolioUrl != null) 'portfolio_url': portfolioUrl,
    };

    final response = await _api.post(
      '${ApiConfig.applications}/applications/',
      body: body,
    );

    return Application.fromJson(jsonDecode(response.body));
  }

  // Retirar aplicación
  Future<void> withdraw(String applicationId) async {
    await _api.delete('${ApiConfig.applications}/applications/$applicationId/');
  }

  // Obtener estadísticas de aplicaciones
  Future<Map<String, dynamic>> getStatistics() async {
    final response = await _api.get(
      '${ApiConfig.applications}/applications/statistics/',
    );

    return jsonDecode(response.body);
  }
}
