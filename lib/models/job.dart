class Job {
  final String id;
  final String title;
  final String companyName;
  final String? companyLogo;
  final String location;
  final bool remoteOk;
  final String jobType; // 'full_time', 'part_time', 'contract', 'internship', 'temporary'
  final String experienceLevel; // 'entry', 'mid', 'senior', 'lead', 'executive'
  final String description;
  final List<String> requirements;
  final List<String> responsibilities;
  final List<String> benefits;
  final List<String> skillsRequired;
  final double? salaryMin;
  final double? salaryMax;
  final String? salaryCurrency;
  final String? applicationUrl;
  final int viewsCount;
  final DateTime postedAt;
  final DateTime? expiresAt;
  final bool isActive;
  final bool isSaved;

  Job({
    required this.id,
    required this.title,
    required this.companyName,
    this.companyLogo,
    required this.location,
    this.remoteOk = false,
    required this.jobType,
    required this.experienceLevel,
    required this.description,
    this.requirements = const [],
    this.responsibilities = const [],
    this.benefits = const [],
    this.skillsRequired = const [],
    this.salaryMin,
    this.salaryMax,
    this.salaryCurrency,
    this.applicationUrl,
    this.viewsCount = 0,
    required this.postedAt,
    this.expiresAt,
    this.isActive = true,
    this.isSaved = false,
  });

  factory Job.fromJson(Map<String, dynamic> json) {
    return Job(
      id: json['id'],
      title: json['title'],
      companyName: json['company_name'],
      companyLogo: json['company_logo'],
      location: json['location'],
      remoteOk: json['remote_ok'] ?? false,
      jobType: json['job_type'],
      experienceLevel: json['experience_level'],
      description: json['description'],
      requirements: json['requirements'] != null 
          ? List<String>.from(json['requirements']) 
          : [],
      responsibilities: json['responsibilities'] != null 
          ? List<String>.from(json['responsibilities']) 
          : [],
      benefits: json['benefits'] != null 
          ? List<String>.from(json['benefits']) 
          : [],
      skillsRequired: json['skills_required'] != null 
          ? List<String>.from(json['skills_required']) 
          : [],
      salaryMin: json['salary_min'] != null 
          ? double.parse(json['salary_min'].toString()) 
          : null,
      salaryMax: json['salary_max'] != null 
          ? double.parse(json['salary_max'].toString()) 
          : null,
      salaryCurrency: json['salary_currency'],
      applicationUrl: json['application_url'],
      viewsCount: json['views_count'] ?? 0,
      postedAt: DateTime.parse(json['posted_at']),
      expiresAt: json['expires_at'] != null 
          ? DateTime.parse(json['expires_at']) 
          : null,
      isActive: json['is_active'] ?? true,
      isSaved: json['is_saved'] ?? false,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'company_name': companyName,
      'company_logo': companyLogo,
      'location': location,
      'remote_ok': remoteOk,
      'job_type': jobType,
      'experience_level': experienceLevel,
      'description': description,
      'requirements': requirements,
      'responsibilities': responsibilities,
      'benefits': benefits,
      'skills_required': skillsRequired,
      'salary_min': salaryMin,
      'salary_max': salaryMax,
      'salary_currency': salaryCurrency,
      'application_url': applicationUrl,
      'views_count': viewsCount,
      'posted_at': postedAt.toIso8601String(),
      'expires_at': expiresAt?.toIso8601String(),
      'is_active': isActive,
      'is_saved': isSaved,
    };
  }

  String get salaryRange {
    if (salaryMin != null && salaryMax != null) {
      final currency = salaryCurrency ?? 'USD';
      return '$currency \$${salaryMin!.toStringAsFixed(0)} - \$${salaryMax!.toStringAsFixed(0)}';
    } else if (salaryMin != null) {
      final currency = salaryCurrency ?? 'USD';
      return '$currency \$${salaryMin!.toStringAsFixed(0)}+';
    }
    return 'Salario no especificado';
  }

  String get jobTypeDisplay {
    switch (jobType) {
      case 'full_time':
        return 'Tiempo completo';
      case 'part_time':
        return 'Medio tiempo';
      case 'contract':
        return 'Contrato';
      case 'internship':
        return 'Pasantía';
      case 'temporary':
        return 'Temporal';
      default:
        return jobType;
    }
  }

  String get experienceLevelDisplay {
    switch (experienceLevel) {
      case 'entry':
        return 'Principiante';
      case 'mid':
        return 'Intermedio';
      case 'senior':
        return 'Senior';
      case 'lead':
        return 'Líder';
      case 'executive':
        return 'Ejecutivo';
      default:
        return experienceLevel;
    }
  }

  Job copyWith({
    String? id,
    String? title,
    String? companyName,
    String? companyLogo,
    String? location,
    bool? remoteOk,
    String? jobType,
    String? experienceLevel,
    String? description,
    List<String>? requirements,
    List<String>? responsibilities,
    List<String>? benefits,
    List<String>? skillsRequired,
    double? salaryMin,
    double? salaryMax,
    String? salaryCurrency,
    String? applicationUrl,
    int? viewsCount,
    DateTime? postedAt,
    DateTime? expiresAt,
    bool? isActive,
    bool? isSaved,
  }) {
    return Job(
      id: id ?? this.id,
      title: title ?? this.title,
      companyName: companyName ?? this.companyName,
      companyLogo: companyLogo ?? this.companyLogo,
      location: location ?? this.location,
      remoteOk: remoteOk ?? this.remoteOk,
      jobType: jobType ?? this.jobType,
      experienceLevel: experienceLevel ?? this.experienceLevel,
      description: description ?? this.description,
      requirements: requirements ?? this.requirements,
      responsibilities: responsibilities ?? this.responsibilities,
      benefits: benefits ?? this.benefits,
      skillsRequired: skillsRequired ?? this.skillsRequired,
      salaryMin: salaryMin ?? this.salaryMin,
      salaryMax: salaryMax ?? this.salaryMax,
      salaryCurrency: salaryCurrency ?? this.salaryCurrency,
      applicationUrl: applicationUrl ?? this.applicationUrl,
      viewsCount: viewsCount ?? this.viewsCount,
      postedAt: postedAt ?? this.postedAt,
      expiresAt: expiresAt ?? this.expiresAt,
      isActive: isActive ?? this.isActive,
      isSaved: isSaved ?? this.isSaved,
    );
  }
}