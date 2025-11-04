import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/user.dart';
import '../providers/auth_provider.dart';

class EditProfileScreen extends StatefulWidget {
  const EditProfileScreen({super.key});

  @override
  State<EditProfileScreen> createState() => _EditProfileScreenState();
}

class _EditProfileScreenState extends State<EditProfileScreen> {
  final _formKey = GlobalKey<FormState>();
  late TextEditingController _nameController;
  late TextEditingController _ageController;
  late TextEditingController _phoneController;
  late TextEditingController _locationController;
  late TextEditingController _experienceController;
  late TextEditingController _educationController;
  late List<String> _skills;
  final TextEditingController _skillController = TextEditingController();
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    final user = Provider.of<AuthProvider>(context, listen: false).user;
    _nameController = TextEditingController(text: user?.name ?? '');
    _ageController = TextEditingController(text: user?.age?.toString() ?? '');
    _phoneController = TextEditingController(text: user?.phone ?? '');
    _locationController = TextEditingController(text: user?.location ?? '');
    _experienceController = TextEditingController(text: user?.experience ?? '');
    _educationController = TextEditingController(text: user?.education ?? '');
    _skills = List.from(user?.skills ?? []);
  }

  @override
  void dispose() {
    _nameController.dispose();
    _ageController.dispose();
    _phoneController.dispose();
    _locationController.dispose();
    _experienceController.dispose();
    _educationController.dispose();
    _skillController.dispose();
    super.dispose();
  }

  Future<void> _saveProfile() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isLoading = true);

    try {
      final authProvider = Provider.of<AuthProvider>(context, listen: false);
      
      final profileData = {
        'name': _nameController.text.trim(),
        'age': _ageController.text.isNotEmpty ? int.parse(_ageController.text) : null,
        'phone': _phoneController.text.trim(),
        'location': _locationController.text.trim(),
        'experience': _experienceController.text.trim(),
        'education': _educationController.text.trim(),
        'skills': _skills,
      };

      await authProvider.updateProfile(profileData);

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Perfil actualizado exitosamente'),
            backgroundColor: Colors.green,
          ),
        );
        Navigator.pop(context);
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error al actualizar perfil: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    } finally {
      if (mounted) {
        setState(() => _isLoading = false);
      }
    }
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
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: Form(
                key: _formKey,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Información Personal
                    const Text(
                      'Información Personal',
                      style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 16),

                    TextFormField(
                      controller: _nameController,
                      decoration: const InputDecoration(
                        labelText: 'Nombre completo *',
                        border: OutlineInputBorder(),
                        prefixIcon: Icon(Icons.person),
                      ),
                      validator: (value) {
                        if (value == null || value.isEmpty) {
                          return 'Por favor ingresa tu nombre';
                        }
                        return null;
                      },
                    ),
                    const SizedBox(height: 16),

                    TextFormField(
                      controller: _ageController,
                      decoration: const InputDecoration(
                        labelText: 'Edad',
                        border: OutlineInputBorder(),
                        prefixIcon: Icon(Icons.cake),
                      ),
                      keyboardType: TextInputType.number,
                      validator: (value) {
                        if (value != null && value.isNotEmpty) {
                          final age = int.tryParse(value);
                          if (age == null || age < 18 || age > 100) {
                            return 'Ingresa una edad válida (18-100)';
                          }
                        }
                        return null;
                      },
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
            ),
    );
  }
}
