class User {
  final String id;
  final String email;
  final String name;
  final int? age;
  final String? phone;
  final String? profileImage;
  final String? resume;
  final String? experience;
  final String? education;
  final String? location;
  final List<String> skills;
  final int points;
  final int profileCompletionPercentage;
  final DateTime? dateJoined;

  User({
    required this.id,
    required this.email,
    required this.name,
    this.age,
    this.phone,
    this.profileImage,
    this.resume,
    this.experience,
    this.education,
    this.location,
    this.skills = const [],
    this.points = 0,
    this.profileCompletionPercentage = 0,
    this.dateJoined,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      email: json['email'],
      name: json['name'],
      age: json['age'],
      phone: json['phone'],
      profileImage: json['profile_image'],
      resume: json['resume'],
      experience: json['experience'],
      education: json['education'],
      location: json['location'],
      skills: json['skills'] != null 
          ? List<String>.from(json['skills']) 
          : [],
      points: json['points'] ?? 0,
      profileCompletionPercentage: json['profile_completion_percentage'] ?? 0,
      dateJoined: json['date_joined'] != null 
          ? DateTime.parse(json['date_joined']) 
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'email': email,
      'name': name,
      'age': age,
      'phone': phone,
      'profile_image': profileImage,
      'resume': resume,
      'experience': experience,
      'education': education,
      'location': location,
      'skills': skills,
      'points': points,
      'profile_completion_percentage': profileCompletionPercentage,
      'date_joined': dateJoined?.toIso8601String(),
    };
  }

  User copyWith({
    String? id,
    String? email,
    String? name,
    int? age,
    String? phone,
    String? profileImage,
    String? resume,
    String? experience,
    String? education,
    String? location,
    List<String>? skills,
    int? points,
    int? profileCompletionPercentage,
    DateTime? dateJoined,
  }) {
    return User(
      id: id ?? this.id,
      email: email ?? this.email,
      name: name ?? this.name,
      age: age ?? this.age,
      phone: phone ?? this.phone,
      profileImage: profileImage ?? this.profileImage,
      resume: resume ?? this.resume,
      experience: experience ?? this.experience,
      education: education ?? this.education,
      location: location ?? this.location,
      skills: skills ?? this.skills,
      points: points ?? this.points,
      profileCompletionPercentage: profileCompletionPercentage ?? this.profileCompletionPercentage,
      dateJoined: dateJoined ?? this.dateJoined,
    );
  }

  @override
  String toString() {
    return 'User(id: $id, name: $name, email: $email, points: $points)';
  }
}