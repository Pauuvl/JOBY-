class Streak {
  final int currentStreak;
  final int longestStreak;
  final DateTime lastActivityDate;
  final List<Activity> activities;
  final int totalPoints;
  final List<AchievementBadge> badges;

  Streak({
    required this.currentStreak,
    required this.longestStreak,
    required this.lastActivityDate,
    required this.activities,
    required this.totalPoints,
    required this.badges,
  });

  bool get isActiveToday {
    final now = DateTime.now();
    return lastActivityDate.year == now.year &&
        lastActivityDate.month == now.month &&
        lastActivityDate.day == now.day;
  }

  factory Streak.initial() {
    return Streak(
      currentStreak: 0,
      longestStreak: 0,
      lastActivityDate: DateTime.now().subtract(const Duration(days: 1)),
      activities: [],
      totalPoints: 0,
      badges: [],
    );
  }

  Streak copyWith({
    int? currentStreak,
    int? longestStreak,
    DateTime? lastActivityDate,
    List<Activity>? activities,
    int? totalPoints,
    List<AchievementBadge>? badges,
  }) {
    return Streak(
      currentStreak: currentStreak ?? this.currentStreak,
      longestStreak: longestStreak ?? this.longestStreak,
      lastActivityDate: lastActivityDate ?? this.lastActivityDate,
      activities: activities ?? this.activities,
      totalPoints: totalPoints ?? this.totalPoints,
      badges: badges ?? this.badges,
    );
  }
}

class Activity {
  final String type; // 'job_applied', 'profile_updated', 'daily_login', 'friend_referred'
  final DateTime date;
  final int points;
  final String description;

  Activity({
    required this.type,
    required this.date,
    required this.points,
    required this.description,
  });
}

class AchievementBadge {
  final String id;
  final String name;
  final String description;
  final String icon;
  final DateTime earnedDate;

  AchievementBadge({
    required this.id,
    required this.name,
    required this.description,
    required this.icon,
    required this.earnedDate,
  });
}
