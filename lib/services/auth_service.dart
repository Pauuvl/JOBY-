import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/user.dart';
import 'api_service.dart';

class AuthService {
  static final AuthService _instance = AuthService._internal();
  factory AuthService() => _instance;
  AuthService._internal();

  final ApiService _api = ApiService();
  User? _currentUser;
  
  User? get currentUser => _currentUser;
  bool get isAuthenticated => _currentUser != null;

  // Inicializar servicio (cargar usuario guardado)
  Future<void> init() async {
    await _api.initTokens();
    
    if (_api.accessToken != null) {
      try {
        await loadCurrentUser();
      } catch (e) {
        // Si falla cargar el usuario, limpiar tokens
        await logout();
      }
    }
  }

  // Registro de usuario
  Future<User> register({
    required String email,
    required String password,
    required String name,
    String? phone,
  }) async {
    try {
      final response = await _api.post(
        '/auth/register/',
        body: {
          'email': email,
          'password': password,
          'name': name,
          if (phone != null) 'phone': phone,
        },
        requiresAuth: false,
      );

      final data = jsonDecode(response.body);
      
      // Guardar tokens
      await _api.saveTokens(
        data['access'],
        data['refresh'],
      );

      // Guardar usuario
      _currentUser = User.fromJson(data['user']);
      await _saveUserLocally(_currentUser!);

      return _currentUser!;
    } catch (e) {
      rethrow;
    }
  }

  // Login
  Future<User> login({
    required String email,
    required String password,
  }) async {
    try {
      final response = await _api.post(
        '/auth/login/',
        body: {
          'email': email,
          'password': password,
        },
        requiresAuth: false,
      );

      final data = jsonDecode(response.body);
      
      // Guardar tokens
      await _api.saveTokens(
        data['access'],
        data['refresh'],
      );

      // Guardar usuario
      _currentUser = User.fromJson(data['user']);
      await _saveUserLocally(_currentUser!);

      return _currentUser!;
    } catch (e) {
      rethrow;
    }
  }

  // Logout
  Future<void> logout() async {
    try {
      // Intentar hacer logout en el servidor
      await _api.post('/auth/logout/');
    } catch (e) {
      // Ignorar errores de logout del servidor
    } finally {
      // Limpiar datos locales
      _currentUser = null;
      await _api.clearTokens();
      await _clearUserLocally();
    }
  }

  // Cargar usuario actual desde el servidor
  Future<User> loadCurrentUser() async {
    try {
      final response = await _api.get('/auth/me/');
      final data = jsonDecode(response.body);
      
      _currentUser = User.fromJson(data);
      await _saveUserLocally(_currentUser!);
      
      return _currentUser!;
    } catch (e) {
      rethrow;
    }
  }

  // Actualizar perfil
  Future<User> updateProfile(Map<String, dynamic> profileData) async {
    try {
      final response = await _api.put('/auth/profile/', body: profileData);
      final data = jsonDecode(response.body);
      
      _currentUser = User.fromJson(data);
      await _saveUserLocally(_currentUser!);
      
      return _currentUser!;
    } catch (e) {
      rethrow;
    }
  }

  // Cambiar contraseña
  Future<void> changePassword({
    required String oldPassword,
    required String newPassword,
  }) async {
    try {
      await _api.post(
        '/auth/change-password/',
        body: {
          'old_password': oldPassword,
          'new_password': newPassword,
        },
      );
    } catch (e) {
      rethrow;
    }
  }

  // Guardar usuario localmente
  Future<void> _saveUserLocally(User user) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('current_user', jsonEncode(user.toJson()));
  }

  // Limpiar usuario local
  Future<void> _clearUserLocally() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('current_user');
  }

  // Cargar usuario local (para restaurar sesión)
  Future<User?> loadUserLocally() async {
    final prefs = await SharedPreferences.getInstance();
    final userJson = prefs.getString('current_user');
    
    if (userJson != null) {
      return User.fromJson(jsonDecode(userJson));
    }
    
    return null;
  }

  // Registrar token FCM para notificaciones push
  Future<void> registerFCMToken(String token) async {
    try {
      await _api.post(
        '/auth/fcm-token/',
        body: {'fcm_token': token},
      );
    } catch (e) {
      // Ignorar errores de registro de token
      print('Error registering FCM token: $e');
    }
  }
}
