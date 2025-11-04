import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../config/api_config.dart';

class ApiService {
  static final ApiService _instance = ApiService._internal();
  factory ApiService() => _instance;
  ApiService._internal();

  final _storage = const FlutterSecureStorage();
  String? _accessToken;
  String? _refreshToken;

  // Getters para los tokens
  String? get accessToken => _accessToken;
  String? get refreshToken => _refreshToken;

  // Inicializar tokens desde el almacenamiento
  Future<void> initTokens() async {
    _accessToken = await _storage.read(key: 'access_token');
    _refreshToken = await _storage.read(key: 'refresh_token');
  }

  // Guardar tokens
  Future<void> saveTokens(String access, String refresh) async {
    _accessToken = access;
    _refreshToken = refresh;
    await _storage.write(key: 'access_token', value: access);
    await _storage.write(key: 'refresh_token', value: refresh);
  }

  // Limpiar tokens
  Future<void> clearTokens() async {
    _accessToken = null;
    _refreshToken = null;
    await _storage.delete(key: 'access_token');
    await _storage.delete(key: 'refresh_token');
  }

  // Headers con autenticación
  Map<String, String> _getHeaders({bool includeAuth = true}) {
    final headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };

    if (includeAuth && _accessToken != null) {
      headers['Authorization'] = 'Bearer $_accessToken';
    }

    return headers;
  }

  // GET request
  Future<http.Response> get(
    String endpoint, {
    Map<String, String>? queryParams,
    bool requiresAuth = true,
  }) async {
    try {
      var uri = Uri.parse('${ApiConfig.baseUrl}$endpoint');
      
      if (queryParams != null && queryParams.isNotEmpty) {
        uri = uri.replace(queryParameters: queryParams);
      }

      final response = await http.get(
        uri,
        headers: _getHeaders(includeAuth: requiresAuth),
      ).timeout(ApiConfig.connectionTimeout);

      return _handleResponse(response);
    } catch (e) {
      throw _handleError(e);
    }
  }

  // POST request
  Future<http.Response> post(
    String endpoint, {
    Map<String, dynamic>? body,
    bool requiresAuth = true,
  }) async {
    try {
      final uri = Uri.parse('${ApiConfig.baseUrl}$endpoint');
      
      final response = await http.post(
        uri,
        headers: _getHeaders(includeAuth: requiresAuth),
        body: body != null ? jsonEncode(body) : null,
      ).timeout(ApiConfig.connectionTimeout);

      return _handleResponse(response);
    } catch (e) {
      throw _handleError(e);
    }
  }

  // PUT request
  Future<http.Response> put(
    String endpoint, {
    Map<String, dynamic>? body,
    bool requiresAuth = true,
  }) async {
    try {
      final uri = Uri.parse('${ApiConfig.baseUrl}$endpoint');
      
      final response = await http.put(
        uri,
        headers: _getHeaders(includeAuth: requiresAuth),
        body: body != null ? jsonEncode(body) : null,
      ).timeout(ApiConfig.connectionTimeout);

      return _handleResponse(response);
    } catch (e) {
      throw _handleError(e);
    }
  }

  // PATCH request
  Future<http.Response> patch(
    String endpoint, {
    Map<String, dynamic>? body,
    bool requiresAuth = true,
  }) async {
    try {
      final uri = Uri.parse('${ApiConfig.baseUrl}$endpoint');
      
      final response = await http.patch(
        uri,
        headers: _getHeaders(includeAuth: requiresAuth),
        body: body != null ? jsonEncode(body) : null,
      ).timeout(ApiConfig.connectionTimeout);

      return _handleResponse(response);
    } catch (e) {
      throw _handleError(e);
    }
  }

  // DELETE request
  Future<http.Response> delete(
    String endpoint, {
    bool requiresAuth = true,
  }) async {
    try {
      final uri = Uri.parse('${ApiConfig.baseUrl}$endpoint');
      
      final response = await http.delete(
        uri,
        headers: _getHeaders(includeAuth: requiresAuth),
      ).timeout(ApiConfig.connectionTimeout);

      return _handleResponse(response);
    } catch (e) {
      throw _handleError(e);
    }
  }

  // Manejar respuestas
  http.Response _handleResponse(http.Response response) {
    if (response.statusCode >= 200 && response.statusCode < 300) {
      return response;
    } else if (response.statusCode == 401) {
      // Intentar obtener mensaje de error del backend
      try {
        final errorData = jsonDecode(response.body);
        throw ApiException(
          errorData['detail'] ?? errorData['error'] ?? errorData['message'] ?? 'No autorizado',
          statusCode: 401,
          data: errorData,
        );
      } catch (e) {
        throw ApiException('No autorizado', statusCode: 401);
      }
    } else if (response.statusCode == 404) {
      throw ApiException('Recurso no encontrado', statusCode: 404);
    } else if (response.statusCode >= 500) {
      throw ApiException('Error del servidor', statusCode: response.statusCode);
    } else {
      final errorData = jsonDecode(response.body);
      throw ApiException(
        errorData['detail'] ?? errorData['error'] ?? 'Error desconocido',
        statusCode: response.statusCode,
        data: errorData,
      );
    }
  }

  // Manejar errores
  Exception _handleError(dynamic error) {
    if (error is ApiException) {
      return error;
    } else if (error is http.ClientException) {
      return ApiException('Error de conexión: ${error.message}');
    } else {
      return ApiException('Error: $error');
    }
  }

  // Refrescar token
  Future<bool> refreshAccessToken() async {
    if (_refreshToken == null) return false;

    try {
      final response = await post(
        '${ApiConfig.auth}/token/refresh/',
        body: {'refresh': _refreshToken},
        requiresAuth: false,
      );

      final data = jsonDecode(response.body);
      _accessToken = data['access'];
      await _storage.write(key: 'access_token', value: _accessToken!);
      
      return true;
    } catch (e) {
      await clearTokens();
      return false;
    }
  }
}

// Excepción personalizada para errores de API
class ApiException implements Exception {
  final String message;
  final int? statusCode;
  final Map<String, dynamic>? data;

  ApiException(this.message, {this.statusCode, this.data});

  @override
  String toString() => message;
}
