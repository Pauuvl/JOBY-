import 'package:flutter/material.dart';
import '../models/job.dart';

class JobSearchScreen extends StatefulWidget {
  final String? searchTerm;
  
  const JobSearchScreen({super.key, this.searchTerm});

  @override
  State<JobSearchScreen> createState() => _JobSearchScreenState();
}

class _JobSearchScreenState extends State<JobSearchScreen> {
  final _searchController = TextEditingController();
  List<Job> _jobs = [];
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    if (widget.searchTerm != null) {
      _searchController.text = widget.searchTerm!;
    }
    _searchJobs();
  }

  void _searchJobs() {
    setState(() => _isLoading = true);
    
    // Simular búsqueda de trabajos
    Future.delayed(const Duration(seconds: 1), () {
      setState(() {
        _jobs = [
          Job(
            id: 1,
            title: 'Desarrollador Flutter Senior',
            company: 'TechCorp',
            location: 'Remoto',
            salary: '\$80,000 - \$100,000',
            description: 'Buscamos un desarrollador Flutter experimentado...',
            requirements: 'Flutter, Dart, Firebase',
            type: 'Remoto',
            postedDate: DateTime.now().subtract(const Duration(days: 2)),
          ),
          Job(
            id: 2,
            title: 'Diseñador UX/UI',
            company: 'StartupXYZ',
            location: 'Madrid, España',
            salary: '\$45,000 - \$60,000',
            description: 'Únete a nuestro equipo de diseño...',
            requirements: 'Figma, Adobe XD, Sketch',
            type: 'Híbrido',
            postedDate: DateTime.now().subtract(const Duration(days: 1)),
          ),
        ];
        _isLoading = false;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Buscar Trabajos'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: TextField(
              controller: _searchController,
              decoration: InputDecoration(
                hintText: 'Buscar trabajos...',
                prefixIcon: const Icon(Icons.search),
                suffixIcon: IconButton(
                  icon: const Icon(Icons.clear),
                  onPressed: () => _searchController.clear(),
                ),
                border: const OutlineInputBorder(),
              ),
              onSubmitted: (_) => _searchJobs(),
            ),
          ),
          Expanded(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator())
                : ListView.builder(
                    itemCount: _jobs.length,
                    itemBuilder: (context, index) => _buildJobCard(_jobs[index]),
                  ),
          ),
        ],
      ),
    );
  }

  Widget _buildJobCard(Job job) {
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: ListTile(
        leading: const CircleAvatar(child: Icon(Icons.business)),
        title: Text(job.title, style: const TextStyle(fontWeight: FontWeight.bold)),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(job.company),
            Text('${job.location} • ${job.type}'),
            Text(job.salary, style: const TextStyle(color: Colors.green)),
          ],
        ),
        onTap: () {
          // Navegar a detalles del trabajo
        },
      ),
    );
  }
}