import 'dart:convert';
import '../models/course.dart';
import '../config/api_config.dart';
import 'api_service.dart';

class CourseService {
  static final CourseService _instance = CourseService._internal();
  factory CourseService() => _instance;
  CourseService._internal();

  final ApiService _api = ApiService();

  // Obtener cursos recomendados
  Future<List<Course>> getRecommendedCourses() async {
    final response = await _api.get('${ApiConfig.auth}/courses/recommended/');
    final responseData = jsonDecode(response.body);
    
    final List<dynamic> data = responseData is Map 
        ? (responseData['results'] ?? responseData)
        : responseData;
    
    return data.map((json) => Course.fromJson(json)).toList();
  }

  // Buscar cursos
  Future<List<Course>> searchCourses(String query) async {
    final response = await _api.get(
      '${ApiConfig.auth}/courses/search/',
      queryParams: {'q': query},
    );
    final responseData = jsonDecode(response.body);
    
    final List<dynamic> data = responseData is Map 
        ? (responseData['results'] ?? responseData['courses'] ?? [])
        : responseData;
    
    return data.map((json) => Course.fromJson(json)).toList();
  }

  // Inscribirse en un curso
  Future<UserCourse> enrollInCourse(String courseId) async {
    final response = await _api.post(
      '${ApiConfig.auth}/user-courses/enroll/',
      body: {'course_id': courseId},
    );
    return UserCourse.fromJson(jsonDecode(response.body));
  }

  // Obtener cursos del usuario en progreso
  Future<List<UserCourse>> getInProgressCourses() async {
    final response = await _api.get('${ApiConfig.auth}/user-courses/in_progress/');
    final responseData = jsonDecode(response.body);
    
    final List<dynamic> data = responseData is Map 
        ? (responseData['results'] ?? [])
        : responseData;
    
    return data.map((json) => UserCourse.fromJson(json)).toList();
  }

  // Obtener cursos completados
  Future<List<UserCourse>> getCompletedCourses() async {
    final response = await _api.get('${ApiConfig.auth}/user-courses/completed/');
    final responseData = jsonDecode(response.body);
    
    final List<dynamic> data = responseData is Map 
        ? (responseData['results'] ?? [])
        : responseData;
    
    return data.map((json) => UserCourse.fromJson(json)).toList();
  }

  // Actualizar progreso del curso
  Future<UserCourse> updateProgress(String enrollmentId, int progress) async {
    final response = await _api.post(
      '${ApiConfig.auth}/user-courses/$enrollmentId/update_progress/',
      body: {'progress_percentage': progress},
    );
    return UserCourse.fromJson(jsonDecode(response.body));
  }

  // Obtener todas las empresas
  Future<List<Company>> getCompanies() async {
    final response = await _api.get('${ApiConfig.auth}/companies/');
    final responseData = jsonDecode(response.body);
    
    final List<dynamic> data = responseData is Map 
        ? (responseData['results'] ?? [])
        : responseData;
    
    return data.map((json) => Company.fromJson(json)).toList();
  }
}
