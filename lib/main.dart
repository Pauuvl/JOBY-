import 'package:flutter/material.dart';
import 'screens/welcome_screen.dart';
import 'screens/login_screen.dart';
import 'screens/register_screen.dart';
import 'screens/home_screen.dart';
import 'screens/profile_setup_screen.dart'; // 👈 nueva pantalla

void main() {
  runApp(JobyApp());
}

class JobyApp extends StatelessWidget {
  // Simulación: aquí decidirías desde tu base de datos o backend
  final bool isLoggedIn = false;       // ¿ya inició sesión?
  final bool isProfileComplete = false; // ¿ya completó su perfil?

  @override
  Widget build(BuildContext context) {
    String initialRoute;

    if (!isLoggedIn) {
      initialRoute = '/'; // Welcome
    } else if (!isProfileComplete) {
      initialRoute = '/profileSetup'; // Completar perfil
    } else {
      initialRoute = '/home'; // Ir a Home
    }

    return MaterialApp(
      debugShowCheckedModeBanner: false,
      initialRoute: initialRoute,
      routes: {
        '/': (context) => WelcomeScreen(),
        '/login': (context) => LoginScreen(),
        '/register': (context) => RegisterScreen(),
        '/profileSetup': (context) => ProfileSetupScreen(), // 👈 agregada
        '/home': (context) => HomeScreen(),
      },
    );
  }
}
