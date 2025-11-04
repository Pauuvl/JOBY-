class Streak {
  final String id;
  final int currentStreak;
  final int longestStreak;
  final DateTime? lastActivityDate;
  final int totalLogins;
  final int totalApplications;
  final int totalProfileUpdates;
  final int totalJobsSaved;
  final int totalJobsViewed;

  Streak({
    required this.id,
    this.currentStreak = 0,
    this.longestStreak = 0,
    this.lastActivityDate,
    this.totalLogins = 0,
    this.totalApplications = 0,
    this.totalProfileUpdates = 0,
    this.totalJobsSaved = 0,
    this.totalJobsViewed = 0,
  });

  factory Streak.fromJson(Map<String, dynamic> json) {
    return Streak(
      id: json['id']?.toString() ?? '',
      currentStreak: json['current_streak'] ?? 0,
      longestStreak: json['longest_streak'] ?? 0,
      lastActivityDate: json['last_activity_date'] != null 
          ? DateTime.parse(json['last_activity_date']) 
          : null,
      totalLogins: json['total_logins'] ?? 0,
      totalApplications: json['total_applications'] ?? 0,
      totalProfileUpdates: json['total_profile_updates'] ?? 0,
      totalJobsSaved: json['total_jobs_saved'] ?? 0,
      totalJobsViewed: json['total_jobs_viewed'] ?? 0,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'current_streak': currentStreak,
      'longest_streak': longestStreak,
      'last_activity_date': lastActivityDate?.toIso8601String(),
      'total_logins': totalLogins,
      'total_applications': totalApplications,
      'total_profile_updates': totalProfileUpdates,
      'total_jobs_saved': totalJobsSaved,
      'total_jobs_viewed': totalJobsViewed,
    };
  }
}

class Achievement {
  final String id;
  final String name;
  final String description;
  final String achievementType;
  final String icon;
  final int pointsReward;
  final String requirementType;
  final int requirementValue;
  final bool isEarned;
  final DateTime? earnedAt;

  Achievement({
    required this.id,
    required this.name,
    required this.description,
    required this.achievementType,
    required this.icon,
    required this.pointsReward,
    required this.requirementType,
    required this.requirementValue,
    this.isEarned = false,
    this.earnedAt,
  });

  factory Achievement.fromJson(Map<String, dynamic> json) {
    return Achievement(
      id: json['id']?.toString() ?? '',
      name: json['name']?.toString() ?? '',
      description: json['description']?.toString() ?? '',
      achievementType: json['achievement_type']?.toString() ?? '',
      icon: json['icon']?.toString() ?? '🏆',
      pointsReward: json['points_reward'] ?? 0,
      requirementType: json['requirement_type']?.toString() ?? '',
      requirementValue: json['requirement_value'] ?? 0,
      isEarned: json['is_earned'] ?? false,
      earnedAt: json['earned_at'] != null 
          ? DateTime.parse(json['earned_at']) 
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'description': description,
      'achievement_type': achievementType,
      'icon': icon,
      'points_reward': pointsReward,
      'requirement_type': requirementType,
      'requirement_value': requirementValue,
      'is_earned': isEarned,
      'earned_at': earnedAt?.toIso8601String(),
    };
  }
}

class PointsHistory {
  final String id;
  final String action;
  final int points;
  final String? description;
  final DateTime createdAt;

  PointsHistory({
    required this.id,
    required this.action,
    required this.points,
    this.description,
    required this.createdAt,
  });

  factory PointsHistory.fromJson(Map<String, dynamic> json) {
    return PointsHistory(
      id: json['id']?.toString() ?? '',
      action: json['action']?.toString() ?? '',
      points: json['points'] ?? 0,
      description: json['description']?.toString(),
      createdAt: json['created_at'] != null 
          ? DateTime.parse(json['created_at'])
          : DateTime.now(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'action': action,
      'points': points,
      'description': description,
      'created_at': createdAt.toIso8601String(),
    };
  }

  String get actionDisplay {
    switch (action) {
      case 'daily_login':
        return 'Inicio de sesión diario';
      case 'profile_update':
        return 'Actualización de perfil';
      case 'job_application':
        return 'Aplicación a empleo';
      case 'achievement_earned':
        return 'Logro obtenido';
      case 'referral':
        return 'Referido';
      default:
        return action;
    }
  }
}

class LeaderboardEntry {
  final String userId;
  final String userName;
  final String? userProfileImage;
  final int rank;
  final int points;
  final String period;

  LeaderboardEntry({
    required this.userId,
    required this.userName,
    this.userProfileImage,
    required this.rank,
    required this.points,
    required this.period,
  });

  factory LeaderboardEntry.fromJson(Map<String, dynamic> json) {
    return LeaderboardEntry(
      userId: (json['user']?['id'] ?? json['user_id'])?.toString() ?? '',
      userName: (json['user']?['name'] ?? json['user_name'])?.toString() ?? 'Usuario',
      userProfileImage: (json['user']?['profile_image'] ?? json['user_profile_image'])?.toString(),
      rank: json['rank'] ?? 0,
      points: json['points'] ?? 0,
      period: json['period']?.toString() ?? 'daily',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'user_id': userId,
      'user_name': userName,
      'user_profile_image': userProfileImage,
      'rank': rank,
      'points': points,
      'period': period,
    };
  }
}

class Challenge {
  final String id;
  final String title;
  final String description;
  final String challengeType;
  final String category;
  final int targetCount;
  final int pointsReward;
  final String icon;
  final bool isActive;
  final DateTime? startDate;
  final DateTime? endDate;
  final bool isAvailable;
  final UserChallenge? userProgress;

  Challenge({
    required this.id,
    required this.title,
    required this.description,
    required this.challengeType,
    required this.category,
    required this.targetCount,
    required this.pointsReward,
    required this.icon,
    this.isActive = true,
    this.startDate,
    this.endDate,
    this.isAvailable = true,
    this.userProgress,
  });

  factory Challenge.fromJson(Map<String, dynamic> json) {
    return Challenge(
      id: json['id']?.toString() ?? '',
      title: json['title']?.toString() ?? '',
      description: json['description']?.toString() ?? '',
      challengeType: json['challenge_type']?.toString() ?? '',
      category: json['category']?.toString() ?? '',
      targetCount: json['target_count'] ?? 0,
      pointsReward: json['points_reward'] ?? 0,
      icon: json['icon']?.toString() ?? '🎯',
      isActive: json['is_active'] ?? true,
      startDate: json['start_date'] != null 
          ? DateTime.parse(json['start_date']) 
          : null,
      endDate: json['end_date'] != null 
          ? DateTime.parse(json['end_date']) 
          : null,
      isAvailable: json['is_available'] ?? true,
      userProgress: json['user_progress'] != null 
          ? UserChallenge.fromJson(json['user_progress']) 
          : null,
    );
  }

  String get typeDisplay {
    switch (challengeType) {
      case 'daily':
        return 'Diario';
      case 'weekly':
        return 'Semanal';
      case 'special':
        return 'Especial';
      default:
        return challengeType;
    }
  }
}

class UserChallenge {
  final String id;
  final String challengeId;
  final Challenge? challengeDetails;
  final int currentProgress;
  final int targetCount;
  final String status;
  final int? pointsEarned;
  final DateTime startedAt;
  final DateTime? completedAt;
  final DateTime? expiresAt;
  final double progressPercentage;
  final bool isCompleted;

  UserChallenge({
    required this.id,
    required this.challengeId,
    this.challengeDetails,
    required this.currentProgress,
    required this.targetCount,
    required this.status,
    this.pointsEarned,
    required this.startedAt,
    this.completedAt,
    this.expiresAt,
    required this.progressPercentage,
    required this.isCompleted,
  });

  factory UserChallenge.fromJson(Map<String, dynamic> json) {
    return UserChallenge(
      id: json['id']?.toString() ?? '',
      challengeId: json['challenge']?.toString() ?? '',
      challengeDetails: json['challenge_details'] != null 
          ? Challenge.fromJson(json['challenge_details']) 
          : null,
      currentProgress: json['current_progress'] ?? 0,
      targetCount: json['challenge_details']?['target_count'] ?? json['target_count'] ?? 0,
      status: json['status']?.toString() ?? 'active',
      pointsEarned: json['points_earned'],
      startedAt: json['started_at'] != null 
          ? DateTime.parse(json['started_at']) 
          : DateTime.now(),
      completedAt: json['completed_at'] != null 
          ? DateTime.parse(json['completed_at']) 
          : null,
      expiresAt: json['expires_at'] != null 
          ? DateTime.parse(json['expires_at']) 
          : null,
      progressPercentage: (json['progress_percentage'] ?? 0.0).toDouble(),
      isCompleted: json['is_completed'] ?? false,
    );
  }

  String get statusDisplay {
    switch (status) {
      case 'active':
        return 'En progreso';
      case 'completed':
        return 'Completado';
      case 'failed':
        return 'Fallido';
      case 'expired':
        return 'Expirado';
      default:
        return status;
    }
  }
}
