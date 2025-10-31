import 'package:flutter/material.dart';
import '../models/user.dart';

class EditProfileScreen extends StatefulWidget {
  final User user;

  const EditProfileScreen({super.key, required this.user});

  @override
  State<EditProfileScreen> createState() => _EditProfileScreenState();
}

class _EditProfileScreenState extends State<EditProfileScreen> {
  late TextEditingController _nameController;
  late TextEditingController _emailController;
  late TextEditingController _phoneController;
  late TextEditingController _locationController;
  late TextEditingController _experienceController;
  late TextEditingController _educationController;
  late List<String> _skills;
  final TextEditingController _skillController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _nameController = TextEditingController(text: widget.user.name);
    _emailController = TextEditingController(text: widget.user.email);
    _phoneController = TextEditingController(text: widget.user.phone ?? '');
    _locationController = TextEditingController(text: widget.user.location ?? '');
    _experienceController = TextEditingController(text: widget.user.experience ?? '');
    _educationController = TextEditingController(text: widget.user.education ?? '');
    _skills = List.from(widget.user.skills);
  }

  @override
  void dispose() {
    _nameController.dispose();
    _emailController.dispose();
    _phoneController.dispose();
    _locationController.dispose();
    _experienceController.dispose();
    _educationController.dispose();
    _skillController.dispose();
    super.dispose();
  }

  void _saveProfile() {
    if (_nameController.text.isEmpty || _emailController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Nombre y email son obligatorios')),
      );
      return;
    }

    final updatedUser = widget.user.copyWith(
      name: _nameController.text,
      email: _emailController.text,
      phone: _phoneController.text.isEmpty ? null : _phoneController.text,
      location: _locationController.text.isEmpty ? null : _locationController.text,
      experience: _experienceController.text.isEmpty ? null : _experienceController.text,
      education: _educationController.text.isEmpty ? null : _educationController.text,
      skills: _skills,
    );

    Navigator.pop(context, updatedUser);
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('Perfil actualizado exitosamente'),
        backgroundColor: Colors.green,
      ),
    );
  }

  void _addSkill() {
    if (_skillController.text.isNotEmpty) {
      setState(() {
        _skills.add(_skillController.text);
        _skillController.clear();
      });
    }
  }

  void _removeSkill(String skill) {
    setState(() {
      _skills.remove(skill);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Editar Perfil'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        actions: [
          IconButton(
            icon: const Icon(Icons.save),
            onPressed: _saveProfile,
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Avatar
            Center(
              child: Stack(
                children: [
                  CircleAvatar(
                    radius: 50,
                    backgroundColor: Theme.of(context).primaryColor,
                    child: widget.user.profileImageUrl != null
                        ? ClipRRect(
                            borderRadius: BorderRadius.circular(50),
                            child: Image.network(widget.user.profileImageUrl!, fit: BoxFit.cover),
                          )
                        : Text(
                            widget.user.name[0].toUpperCase(),
                            style: const TextStyle(fontSize: 32, color: Colors.white),
                          ),
                  ),
                  Positioned(
                    bottom: 0,
                    right: 0,
                    child: CircleAvatar(
                      radius: 18,
                      backgroundColor: Colors.blue,
                      child: IconButton(
                        icon: const Icon(Icons.camera_alt, size: 16, color: Colors.white),
                        onPressed: () {
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(content: Text('Cambiar foto (Próximamente)')),
                          );
                        },
                        padding: EdgeInsets.zero,
                      ),
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 32),

            // Información Personal
            const Text(
              'Información Personal',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),

            TextField(
              controller: _nameController,
              decoration: const InputDecoration(
                labelText: 'Nombre completo *',
                border: OutlineInputBorder(),
                prefixIcon: Icon(Icons.person),
              ),
            ),
            const SizedBox(height: 16),

            TextField(
              controller: _emailController,
              keyboardType: TextInputType.emailAddress,
              decoration: const InputDecoration(
                labelText: 'Email *',
                border: OutlineInputBorder(),
                prefixIcon: Icon(Icons.email),
              ),
            ),
            const SizedBox(height: 16),

            TextField(
              controller: _phoneController,
              keyboardType: TextInputType.phone,
              decoration: const InputDecoration(
                labelText: 'Teléfono',
                border: OutlineInputBorder(),
                prefixIcon: Icon(Icons.phone),
              ),
            ),
            const SizedBox(height: 16),

            TextField(
              controller: _locationController,
              decoration: const InputDecoration(
                labelText: 'Ubicación',
                border: OutlineInputBorder(),
                prefixIcon: Icon(Icons.location_on),
              ),
            ),

            const SizedBox(height: 32),

            // Experiencia Profesional
            const Text(
              'Experiencia Profesional',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),

            TextField(
              controller: _experienceController,
              maxLines: 4,
              decoration: const InputDecoration(
                labelText: 'Experiencia',
                border: OutlineInputBorder(),
                hintText: 'Describe tu experiencia laboral...',
              ),
            ),

            const SizedBox(height: 32),

            // Educación
            const Text(
              'Educación',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),

            TextField(
              controller: _educationController,
              maxLines: 3,
              decoration: const InputDecoration(
                labelText: 'Educación',
                border: OutlineInputBorder(),
                hintText: 'Describe tu formación académica...',
              ),
            ),

            const SizedBox(height: 32),

            // Habilidades
            const Text(
              'Habilidades',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),

            Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _skillController,
                    decoration: const InputDecoration(
                      labelText: 'Nueva habilidad',
                      border: OutlineInputBorder(),
                      hintText: 'Ej: Flutter, React, Python',
                    ),
                    onSubmitted: (_) => _addSkill(),
                  ),
                ),
                const SizedBox(width: 8),
                ElevatedButton(
                  onPressed: _addSkill,
                  child: const Icon(Icons.add),
                ),
              ],
            ),

            const SizedBox(height: 16),

            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: _skills
                  .map(
                    (skill) => Chip(
                      label: Text(skill),
                      deleteIcon: const Icon(Icons.close, size: 18),
                      onDeleted: () => _removeSkill(skill),
                      backgroundColor: Theme.of(context).primaryColor.withOpacity(0.1),
                    ),
                  )
                  .toList(),
            ),

            const SizedBox(height: 32),

            // Botón guardar
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _saveProfile,
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
                child: const Text(
                  'Guardar Cambios',
                  style: TextStyle(fontSize: 18),
                ),
              ),
            ),

            const SizedBox(height: 16),
          ],
        ),
      ),
    );
  }
}
