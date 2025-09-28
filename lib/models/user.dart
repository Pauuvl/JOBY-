class User {
  final int id;
  final String name;
  final String email;
  final String? phone;
  final String? profileImageUrl;
  final String? resume;
  final List<String> skills;
  final String? experience;
  final String? education;
  final String? location;
  final DateTime createdAt;
  final bool isActive;

  User({
    required this.id,
    required this.name,
    required this.email,
    this.phone,
    this.profileImageUrl,
    this.resume,
    this.skills = const [],
    this.experience,
    this.education,
    this.location,
    required this.createdAt,
    this.isActive = true,
  });

  // Método para convertir de JSON (útil para APIs)
  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      name: json['name'],
      email: json['email'],
      phone: json['phone'],
      profileImageUrl: json['profileImageUrl'],
      resume: json['resume'],
      skills: List<String>.from(json['skills'] ?? []),
      experience: json['experience'],
      education: json['education'],
      location: json['location'],
      createdAt: DateTime.parse(json['createdAt']),
      isActive: json['isActive'] ?? true,
    );
  }

  // Método para convertir a JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'email': email,
      'phone': phone,
      'profileImageUrl': profileImageUrl,
      'resume': resume,
      'skills': skills,
      'experience': experience,
      'education': education,
      'location': location,
      'createdAt': createdAt.toIso8601String(),
      'isActive': isActive,
    };
  }

  // Método para crear una copia con cambios
  User copyWith({
    int? id,
    String? name,
    String? email,
    String? phone,
    String? profileImageUrl,
    String? resume,
    List<String>? skills,
    String? experience,
    String? education,
    String? location,
    DateTime? createdAt,
    bool? isActive,
  }) {
    return User(
      id: id ?? this.id,
      name: name ?? this.name,
      email: email ?? this.email,
      phone: phone ?? this.phone,
      profileImageUrl: profileImageUrl ?? this.profileImageUrl,
      resume: resume ?? this.resume,
      skills: skills ?? this.skills,
      experience: experience ?? this.experience,
      education: education ?? this.education,
      location: location ?? this.location,
      createdAt: createdAt ?? this.createdAt,
      isActive: isActive ?? this.isActive,
    );
  }

  // Usuario demo para pruebas
  static User demo() {
    return User(
      id: 1,
      name: 'Usuario Demo',
      email: 'usuario@demo.com',
      phone: '+34 123 456 789',
      skills: ['Flutter', 'Dart', 'Firebase', 'Git'],
      experience: '3 años como desarrollador móvil',
      education: 'Ingeniería en Sistemas',
      location: 'Madrid, España',
      createdAt: DateTime.now().subtract(const Duration(days: 30)),
    );
  }

  @override
  String toString() {
    return 'User(id: $id, name: $name, email: $email)';
  }
}