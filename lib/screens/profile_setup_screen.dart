import 'package:flutter/material.dart';

class ProfileSetupScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Completa tu perfil")),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text("Aquí el usuario completa su perfil"),
            ElevatedButton(
              onPressed: () {
                // Simulación: cuando termine, mandarlo al home
                Navigator.pushReplacementNamed(context, '/home');
              },
              child: Text("Guardar y continuar"),
            ),
          ],
        ),
      ),
    );
  }
}
