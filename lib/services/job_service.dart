import 'dart:convert';
import '../models/job.dart';
import '../config/api_config.dart';
import 'api_service.dart';

class JobService {
  static final JobService _instance = JobService._internal();
  factory JobService() => _instance;
  JobService._internal();

  final ApiService _api = ApiService();

  // Obtener lista de empleos
  Future<List<Job>> getJobs({
    String? jobType,
    String? experienceLevel,
    bool? remoteOk,
    List<String>? skills,
    double? minSalary,
    double? maxSalary,
    String? company,
    String? search,
    String? ordering,
    int? limit,
  }) async {
    final queryParams = <String, String>{};
    
    if (jobType != null) queryParams['job_type'] = jobType;
    if (experienceLevel != null) queryParams['experience_level'] = experienceLevel;
    if (remoteOk != null) queryParams['remote_ok'] = remoteOk.toString();
    if (skills != null && skills.isNotEmpty) queryParams['skills'] = skills.join(',');
    if (minSalary != null) queryParams['min_salary'] = minSalary.toString();
    if (maxSalary != null) queryParams['max_salary'] = maxSalary.toString();
    if (company != null) queryParams['company'] = company;
    if (search != null) queryParams['search'] = search;
    if (ordering != null) queryParams['ordering'] = ordering;
    if (limit != null) queryParams['limit'] = limit.toString();

    final response = await _api.get(
      '${ApiConfig.jobs}/jobs/',
      queryParams: queryParams,
    );

    final data = jsonDecode(response.body);
    final results = data['results'] ?? data;
    
    return (results as List).map((json) => Job.fromJson(json)).toList();
  }

  // Obtener detalle de un empleo
  Future<Job> getJob(String jobId) async {
    final response = await _api.get('${ApiConfig.jobs}/jobs/$jobId/');
    return Job.fromJson(jsonDecode(response.body));
  }

  // Empleos recomendados
  Future<List<Job>> getRecommendedJobs() async {
    final response = await _api.get('${ApiConfig.jobs}/jobs/recommended/');
    final List<dynamic> data = jsonDecode(response.body);
    return data.map((json) => Job.fromJson(json)).toList();
  }

  // Mis empleos publicados
  Future<List<Job>> getMyJobs() async {
    final response = await _api.get('${ApiConfig.jobs}/jobs/my_jobs/');
    final List<dynamic> data = jsonDecode(response.body);
    return data.map((json) => Job.fromJson(json)).toList();
  }

  // Guardar/Des guardar empleo
  Future<void> toggleSaveJob(String jobId) async {
    await _api.post('${ApiConfig.jobs}/jobs/$jobId/save/');
  }

  // Obtener empleos guardados
  Future<List<Job>> getSavedJobs() async {
    final response = await _api.get('${ApiConfig.jobs}/saved-jobs/');
    final List<dynamic> data = jsonDecode(response.body);
    return data.map((json) => Job.fromJson(json['job'])).toList();
  }

  // Crear empleo (para empleadores)
  Future<Job> createJob({
    required String title,
    required String companyName,
    String? companyLogo,
    required String location,
    bool remoteOk = false,
    required String jobType,
    required String experienceLevel,
    required String description,
    List<String>? requirements,
    List<String>? responsibilities,
    List<String>? benefits,
    List<String>? skillsRequired,
    double? salaryMin,
    double? salaryMax,
    String? salaryCurrency,
    String? applicationUrl,
    DateTime? expiresAt,
  }) async {
    final body = {
      'title': title,
      'company_name': companyName,
      if (companyLogo != null) 'company_logo': companyLogo,
      'location': location,
      'remote_ok': remoteOk,
      'job_type': jobType,
      'experience_level': experienceLevel,
      'description': description,
      if (requirements != null) 'requirements': requirements,
      if (responsibilities != null) 'responsibilities': responsibilities,
      if (benefits != null) 'benefits': benefits,
      if (skillsRequired != null) 'skills_required': skillsRequired,
      if (salaryMin != null) 'salary_min': salaryMin,
      if (salaryMax != null) 'salary_max': salaryMax,
      if (salaryCurrency != null) 'salary_currency': salaryCurrency,
      if (applicationUrl != null) 'application_url': applicationUrl,
      if (expiresAt != null) 'expires_at': expiresAt.toIso8601String(),
    };

    final response = await _api.post('${ApiConfig.jobs}/jobs/', body: body);
    return Job.fromJson(jsonDecode(response.body));
  }
}
