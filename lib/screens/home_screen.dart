import 'package:flutter/material.dart';
import '../models/user_profile.dart';

class HomeScreen extends StatelessWidget {
  final UserProfile user;

  HomeScreen({required this.user});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Joby - Página Principal")),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 🔹 Perfil resumido
            Card(
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              elevation: 3,
              child: ListTile(
                leading: CircleAvatar(
                  backgroundColor: Colors.blue,
                  child: Icon(Icons.person, color: Colors.white),
                ),
                title: Text(user.name, style: TextStyle(fontWeight: FontWeight.bold)),
                subtitle: Text("Ingeniería de sistemas"),
                trailing: Icon(Icons.edit),
              ),
            ),
            SizedBox(height: 20),

            // 🔹 Conexiones / Perfiles recomendados
            Text("Mira los perfiles parecidos al tuyo", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            SizedBox(height: 8),
            Card(
              elevation: 2,
              child: ListTile(
                leading: Icon(Icons.people, color: Colors.green),
                title: Text("Conexiones"),
                subtitle: Text("Yilmar Jordán - Microsoft\nCristian Cabreras - Google"),
              ),
            ),
            SizedBox(height: 20),

            // 🔹 Cursos recomendados
            Text("Cursos recomendados del día", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            SizedBox(height: 8),
            Card(
              elevation: 2,
              child: ListTile(
                leading: Icon(Icons.school, color: Colors.blue),
                title: Text("Google recomienda: Introducción a la Analítica de Datos"),
              ),
            ),
            SizedBox(height: 20),

            // 🔹 Progreso
            Text("Progreso", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            SizedBox(height: 8),
            Card(
              elevation: 2,
              child: ListTile(
                leading: Icon(Icons.flag, color: Colors.orange),
                title: Text("10 días de racha"),
                subtitle: Text("Retos completados: 15 este mes"),
              ),
            ),
            SizedBox(height: 20),

            // 🔹 Retos disponibles
            Text("Retos disponibles", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            SizedBox(height: 8),
            Card(
              elevation: 2,
              child: ListTile(
                leading: Icon(Icons.task_alt, color: Colors.purple),
                title: Text("Actualiza tu CV digital"),
                subtitle: Text("Fecha límite: Hoy"),
              ),
            ),
            Card(
              elevation: 2,
              child: ListTile(
                leading: Icon(Icons.task_alt, color: Colors.purple),
                title: Text("Finaliza el curso de Excel para principiantes"),
                subtitle: Text("Fecha límite: Esta semana"),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
