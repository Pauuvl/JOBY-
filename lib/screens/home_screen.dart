import 'package:flutter/material.dart';
import 'job_search_screen.dart';
import 'profile_screen.dart';

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
    const ProfileScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _screens[_selectedIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: (index) => setState(() => _selectedIndex = index),
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
        title: const Text('Joby'), // 👈 CAMBIO AQUÍ (era 'JobFinder')
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
            _buildFeaturedJobs(),
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

  Widget _buildFeaturedJobs() {
    return Column(
      children: [
        _buildJobCard('Desarrollador Flutter Senior', 'TechCorp', 'Remoto', '\$80,000 - \$100,000'),
        _buildJobCard('Diseñador UX/UI', 'StartupXYZ', 'Madrid, España', '\$45,000 - \$60,000'),
        _buildJobCard('Project Manager', 'BigCompany', 'Barcelona, España', '\$55,000 - \$70,000'),
      ],
    );
  }

  Widget _buildJobCard(String title, String company, String location, String salary) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: ListTile(
        leading: const CircleAvatar(
          child: Icon(Icons.business),
        ),
        title: Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(company),
            Text(location, style: const TextStyle(color: Colors.grey)),
          ],
        ),
        trailing: Text(salary, style: const TextStyle(color: Colors.green, fontWeight: FontWeight.bold)),
        onTap: () {
          // Navegar a detalles del trabajo
        },
      ),
    );
  }
}