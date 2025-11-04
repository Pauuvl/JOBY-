import 'package:flutter/foundation.dart' show kIsWeb;

class ApiConfig {
  // URL base del backend Django
  // Para web usa localhost:8000
  // Para emulador Android usa 10.0.2.2 (es el localhost de tu PC)
  // Para dispositivo físico usa la IP de tu PC en la red local
  static String get baseUrl {
    if (kIsWeb) {
      // Para Flutter Web
      return 'http://localhost:8000/api';
    } else {
      // Para Android/iOS (emulador)
      return 'http://10.0.2.2:8000/api';
    }
  }
  
  // Endpoints
  static const String auth = '/auth';
  static const String jobs = '/jobs';
  static const String applications = '/applications';
  static const String streaks = '/streaks';
  static const String notifications = '/notifications';
  
  // Timeouts
  static const Duration connectionTimeout = Duration(seconds: 30);
  static const Duration receiveTimeout = Duration(seconds: 30);
}
