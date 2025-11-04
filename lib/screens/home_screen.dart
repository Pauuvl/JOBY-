import 'package:flutter/material.dart';
import 'job_search_screen.dart';
import 'profile_screen.dart';
import 'job_detail_screen.dart';
import 'streak_screen.dart';
import '../models/job.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _selectedIndex = 0;
  
  final List<Widget> _screens = [
    const HomeTab(),
    const JobSearchScreen(),
    const StreakScreen(),
    const ProfileScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _screens[_selectedIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: (index) => setState(() => _selectedIndex = index),
        type: BottomNavigationBarType.fixed,
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: 'Inicio',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.search),
            label: 'Buscar',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.whatshot),
            label: 'Rachas',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.person),
            label: 'Perfil',
          ),
        ],
      ),
    );
  }
}

class HomeTab extends StatelessWidget {
  const HomeTab({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Joby'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              '¡Hola! Encuentra tu próximo trabajo',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 20),
            _buildQuickSearchCard(context),
            const SizedBox(height: 20),
            const Text(
              'Trabajos Destacados',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            _buildFeaturedJobs(context),
          ],
        ),
      ),
    );
  }

  Widget _buildQuickSearchCard(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            const Text(
              'Búsqueda Rápida',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            TextField(
              decoration: const InputDecoration(
                hintText: 'Ej: Desarrollador Flutter',
                prefixIcon: Icon(Icons.search),
                border: OutlineInputBorder(),
              ),
              onSubmitted: (value) {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => JobSearchScreen(searchTerm: value),
                  ),
                );
              },
            ),
            const SizedBox(height: 16),
            Wrap(
              spacing: 8,
              children: [
                FilterChip(label: const Text('Remoto'), onSelected: (_) {}),
                FilterChip(label: const Text('Tiempo Completo'), onSelected: (_) {}),
                FilterChip(label: const Text('Desarrollo'), onSelected: (_) {}),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFeaturedJobs(BuildContext context) {
    final featuredJobs = [
      Job(
        id: '1',
        title: 'Desarrollador Flutter Senior',
        companyName: 'TechCorp',
        location: 'Remoto',
        salaryMin: 80000,
        salaryMax: 100000,
        description: 'Buscamos un desarrollador Flutter experimentado para liderar el desarrollo de aplicaciones móviles innovadoras. Trabajarás con un equipo dinámico en proyectos de alto impacto.',
        requirements: [
          '5+ años de experiencia en Flutter/Dart',
          'Conocimiento de arquitectura limpia',
          'Experiencia con Firebase y APIs REST',
          'Trabajo en equipo y comunicación efectiva'
        ],
        jobType: 'full_time',
        experienceLevel: 'senior',
        skillsRequired: ['Flutter', 'Dart', 'Firebase'],
        remoteOk: true,
        postedAt: DateTime.now().subtract(const Duration(days: 2)),
      ),
      Job(
        id: '2',
        title: 'Diseñador UX/UI',
        companyName: 'StartupXYZ',
        location: 'Madrid, España',
        salaryMin: 45000,
        salaryMax: 60000,
        description: 'Únete a nuestro equipo de diseño para crear experiencias de usuario excepcionales. Participarás en todo el proceso de diseño desde la investigación hasta la implementación.',
        requirements: [
          'Portfolio sólido de proyectos UX/UI',
          'Dominio de Figma, Adobe XD y Sketch',
          'Conocimiento de principios de diseño',
          'Experiencia en diseño móvil'
        ],
        jobType: 'full_time',
        experienceLevel: 'mid_level',
        skillsRequired: ['Figma', 'Adobe XD', 'UX Design'],
        remoteOk: false,
        postedAt: DateTime.now().subtract(const Duration(days: 1)),
      ),
      Job(
        id: '3',
        title: 'Project Manager',
        companyName: 'BigCompany',
        location: 'Barcelona, España',
        salaryMin: 55000,
        salaryMax: 70000,
        description: 'Gestiona proyectos tecnológicos de principio a fin, coordinando equipos multidisciplinarios y asegurando la entrega exitosa de soluciones innovadoras.',
        requirements: [
          '3+ años gestionando proyectos de TI',
          'Certificación PMP o similar',
          'Metodologías ágiles (Scrum, Kanban)',
          'Excelentes habilidades de liderazgo'
        ],
        jobType: 'full_time',
        experienceLevel: 'mid_level',
        skillsRequired: ['Project Management', 'Scrum', 'Agile'],
        remoteOk: false,
        postedAt: DateTime.now().subtract(const Duration(days: 3)),
      ),
    ];

    return Column(
      children: featuredJobs.map((job) => _buildJobCard(context, job)).toList(),
    );
  }

  Widget _buildJobCard(BuildContext context, Job job) {
    final salary = job.salaryMin != null && job.salaryMax != null
        ? '\$${job.salaryMin!.toInt()}k - \$${job.salaryMax!.toInt()}k'
        : 'Salario competitivo';
    
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: ListTile(
        leading: const CircleAvatar(
          child: Icon(Icons.business),
        ),
        title: Text(job.title, style: const TextStyle(fontWeight: FontWeight.bold)),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(job.companyName),
            Text(job.location, style: const TextStyle(color: Colors.grey)),
          ],
        ),
        trailing: Text(salary, style: const TextStyle(color: Colors.green, fontWeight: FontWeight.bold)),
        onTap: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => JobDetailScreen(job: job),
            ),
          );
        },
      ),
    );
  }
}