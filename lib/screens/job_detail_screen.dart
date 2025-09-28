import 'package:flutter/material.dart';

class JobDetailScreen extends StatelessWidget {
  const JobDetailScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Detalles del Trabajo'),
      ),
      body: const Center(
        child: Text('Pantalla de detalles en construcción...'),
      ),
    );
  }
}