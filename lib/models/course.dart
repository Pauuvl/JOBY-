class Company {
  final String id;
  final String name;
  final String? logoUrl;
  final String? website;
  final String description;

  Company({
    required this.id,
    required this.name,
    this.logoUrl,
    this.website,
    required this.description,
  });

  factory Company.fromJson(Map<String, dynamic> json) {
    return Company(
      id: json['id'],
      name: json['name'],
      logoUrl: json['logo_url'],
      website: json['website'],
      description: json['description'] ?? '',
    );
  }
}

class Course {
  final String id;
  final String title;
  final String description;
  final Company company;
  final List<String> requiredSkills;
  final List<String> skillsTaught;
  final String level;
  final int durationValue;
  final String durationUnit;
  final String durationDisplay;
  final String courseUrl;
  final String? thumbnailUrl;
  final bool isFree;
  final double? price;
  final String currency;
  final double rating;
  final int enrollments;
  final int matchScore;
  final DateTime createdAt;

  Course({
    required this.id,
    required this.title,
    required this.description,
    required this.company,
    required this.requiredSkills,
    required this.skillsTaught,
    required this.level,
    required this.durationValue,
    required this.durationUnit,
    required this.durationDisplay,
    required this.courseUrl,
    this.thumbnailUrl,
    required this.isFree,
    this.price,
    required this.currency,
    required this.rating,
    required this.enrollments,
    required this.matchScore,
    required this.createdAt,
  });

  factory Course.fromJson(Map<String, dynamic> json) {
    return Course(
      id: json['id'],
      title: json['title'],
      description: json['description'],
      company: Company.fromJson(json['company']),
      requiredSkills: List<String>.from(json['required_skills'] ?? []),
      skillsTaught: List<String>.from(json['skills_taught'] ?? []),
      level: json['level'],
      durationValue: json['duration_value'],
      durationUnit: json['duration_unit'],
      durationDisplay: json['duration_display'],
      courseUrl: json['course_url'],
      thumbnailUrl: json['thumbnail_url'],
      isFree: json['is_free'] ?? false,
      price: json['price'] != null ? double.parse(json['price'].toString()) : null,
      currency: json['currency'] ?? 'USD',
      rating: double.parse(json['rating'].toString()),
      enrollments: json['enrollments'] ?? 0,
      matchScore: json['match_score'] ?? 0,
      createdAt: DateTime.parse(json['created_at']),
    );
  }

  String get levelDisplay {
    switch (level) {
      case 'beginner':
        return 'Principiante';
      case 'intermediate':
        return 'Intermedio';
      case 'advanced':
        return 'Avanzado';
      case 'expert':
        return 'Experto';
      default:
        return level;
    }
  }

  String get priceDisplay {
    if (isFree) return 'Gratis';
    if (price == null) return 'Precio no disponible';
    return '\$$price $currency';
  }
}

class UserCourse {
  final String id;
  final Course course;
  final String status;
  final int progressPercentage;
  final DateTime enrolledAt;
  final DateTime? completedAt;

  UserCourse({
    required this.id,
    required this.course,
    required this.status,
    required this.progressPercentage,
    required this.enrolledAt,
    this.completedAt,
  });

  factory UserCourse.fromJson(Map<String, dynamic> json) {
    return UserCourse(
      id: json['id'],
      course: Course.fromJson(json['course']),
      status: json['status'],
      progressPercentage: json['progress_percentage'] ?? 0,
      enrolledAt: DateTime.parse(json['enrolled_at']),
      completedAt: json['completed_at'] != null 
          ? DateTime.parse(json['completed_at']) 
          : null,
    );
  }

  String get statusDisplay {
    switch (status) {
      case 'enrolled':
        return 'Inscrito';
      case 'in_progress':
        return 'En progreso';
      case 'completed':
        return 'Completado';
      case 'abandoned':
        return 'Abandonado';
      default:
        return status;
    }
  }
}
