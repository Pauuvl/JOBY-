class Challenge {
  final String id;
  final String title;
  final String description;
  final String icon;
  final String challengeType; // daily, weekly, special
  final String category; // applications, profile, learning, networking, streak, exploration
  final String targetAction;
  final int targetCount;
  final int pointsReward;
  final double bonusMultiplier;
  final bool isActive;
  final DateTime? startDate;
  final DateTime? endDate;
  final int priority;
  final DateTime createdAt;

  Challenge({
    required this.id,
    required this.title,
    required this.description,
    required this.icon,
    required this.challengeType,
    required this.category,
    required this.targetAction,
    required this.targetCount,
    required this.pointsReward,
    required this.bonusMultiplier,
    required this.isActive,
    this.startDate,
    this.endDate,
    required this.priority,
    required this.createdAt,
  });

  factory Challenge.fromJson(Map<String, dynamic> json) {
    return Challenge(
      id: json['id'],
      title: json['title'],
      description: json['description'],
      icon: json['icon'] ?? '🎯',
      challengeType: json['challenge_type'],
      category: json['category'],
      targetAction: json['target_action'],
      targetCount: json['target_count'],
      pointsReward: json['points_reward'],
      bonusMultiplier: (json['bonus_multiplier'] ?? 1.0).toDouble(),
      isActive: json['is_active'] ?? true,
      startDate: json['start_date'] != null ? DateTime.parse(json['start_date']) : null,
      endDate: json['end_date'] != null ? DateTime.parse(json['end_date']) : null,
      priority: json['priority'] ?? 0,
      createdAt: DateTime.parse(json['created_at']),
    );
  }

  String get typeDisplay {
    switch (challengeType) {
      case 'daily':
        return 'Reto Diario';
      case 'weekly':
        return 'Reto Semanal';
      case 'special':
        return 'Reto Especial';
      default:
        return challengeType;
    }
  }

  String get categoryDisplay {
    switch (category) {
      case 'applications':
        return 'Aplicaciones';
      case 'profile':
        return 'Perfil';
      case 'learning':
        return 'Aprendizaje';
      case 'networking':
        return 'Networking';
      case 'streak':
        return 'Racha';
      case 'exploration':
        return 'Exploración';
      default:
        return category;
    }
  }
}

class UserChallenge {
  final String id;
  final String userId;
  final Challenge challenge;
  final int currentProgress;
  final String status; // active, completed, expired, abandoned
  final DateTime startedAt;
  final DateTime? completedAt;
  final DateTime? expiresAt;
  final int pointsEarned;

  UserChallenge({
    required this.id,
    required this.userId,
    required this.challenge,
    required this.currentProgress,
    required this.status,
    required this.startedAt,
    this.completedAt,
    this.expiresAt,
    required this.pointsEarned,
  });

  factory UserChallenge.fromJson(Map<String, dynamic> json) {
    return UserChallenge(
      id: json['id'],
      userId: json['user'],
      challenge: Challenge.fromJson(json['challenge']),
      currentProgress: json['current_progress'] ?? 0,
      status: json['status'],
      startedAt: DateTime.parse(json['started_at']),
      completedAt: json['completed_at'] != null 
          ? DateTime.parse(json['completed_at']) 
          : null,
      expiresAt: json['expires_at'] != null 
          ? DateTime.parse(json['expires_at']) 
          : null,
      pointsEarned: json['points_earned'] ?? 0,
    );
  }

  int get progressPercentage {
    if (challenge.targetCount == 0) return 0;
    return ((currentProgress / challenge.targetCount) * 100).round().clamp(0, 100);
  }

  bool get isCompleted => currentProgress >= challenge.targetCount;

  String get statusDisplay {
    switch (status) {
      case 'active':
        return 'Activo';
      case 'completed':
        return 'Completado';
      case 'expired':
        return 'Expirado';
      case 'abandoned':
        return 'Abandonado';
      default:
        return status;
    }
  }

  String get timeAgo {
    final now = DateTime.now();
    final difference = now.difference(completedAt ?? startedAt);

    if (difference.inSeconds < 60) {
      return 'Hace un momento';
    } else if (difference.inMinutes < 60) {
      final minutes = difference.inMinutes;
      return 'Hace $minutes ${minutes == 1 ? "minuto" : "minutos"}';
    } else if (difference.inHours < 24) {
      final hours = difference.inHours;
      return 'Hace $hours ${hours == 1 ? "hora" : "horas"}';
    } else if (difference.inDays < 7) {
      final days = difference.inDays;
      return 'Hace $days ${days == 1 ? "día" : "días"}';
    } else if (difference.inDays < 30) {
      final weeks = (difference.inDays / 7).floor();
      return 'Hace $weeks ${weeks == 1 ? "semana" : "semanas"}';
    } else {
      final months = (difference.inDays / 30).floor();
      return 'Hace $months ${months == 1 ? "mes" : "meses"}';
    }
  }
}
