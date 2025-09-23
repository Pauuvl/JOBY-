import 'package:flutter/material.dart';

class RegisterScreen extends StatelessWidget {
  final TextEditingController nameController = TextEditingController();
  final TextEditingController lastNameController = TextEditingController();
  final TextEditingController emailController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Regístrate")),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: SingleChildScrollView(
          child: Column(
            children: [
              TextField(controller: nameController, decoration: InputDecoration(labelText: "Nombre")),
              const SizedBox(height: 12),
              TextField(controller: lastNameController, decoration: InputDecoration(labelText: "Apellido")),
              const SizedBox(height: 12),
              TextField(controller: emailController, decoration: InputDecoration(labelText: "Email")),
              const SizedBox(height: 12),
              TextField(controller: passwordController, decoration: InputDecoration(labelText: "Contraseña"), obscureText: true),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: () {
                  Navigator.pushReplacementNamed(context, '/home');
                },
                child: Text("Registrarse"),
                style: ElevatedButton.styleFrom(
                    minimumSize: Size(double.infinity, 50)),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
