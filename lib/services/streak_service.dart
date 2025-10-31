import '../models/streak.dart';

class StreakService {
  static final StreakService _instance = StreakService._internal();
  factory StreakService() => _instance;
  StreakService._internal();

  Streak _currentStreak = Streak.initial();

  Streak get currentStreak => _currentStreak;

  // Registrar actividad y actualizar racha
  void recordActivity(String type, String description, {int points = 10}) {
    final now = DateTime.now();
    final activity = Activity(
      type: type,
      date: now,
      points: points,
      description: description,
    );

    // Actualizar racha
    int newStreak = _currentStreak.currentStreak;
    if (!_currentStreak.isActiveToday) {
      final daysSinceLastActivity = now.difference(_currentStreak.lastActivityDate).inDays;
      if (daysSinceLastActivity == 1) {
        // Continuar racha
        newStreak++;
      } else if (daysSinceLastActivity > 1) {
        // Racha rota
        newStreak = 1;
      }
    }

    final newLongestStreak = newStreak > _currentStreak.longestStreak ? newStreak : _currentStreak.longestStreak;
    final newActivities = [..._currentStreak.activities, activity];
    final newPoints = _currentStreak.totalPoints + points;

    // Verificar nuevas insignias
    final newBadges = _checkNewBadges(newStreak, newActivities.length, newPoints);

    _currentStreak = _currentStreak.copyWith(
      currentStreak: newStreak,
      longestStreak: newLongestStreak,
      lastActivityDate: now,
      activities: newActivities,
      totalPoints: newPoints,
      badges: [..._currentStreak.badges, ...newBadges],
    );
  }

  List<AchievementBadge> _checkNewBadges(int streak, int activitiesCount, int points) {
    final newBadges = <AchievementBadge>[];
    final earnedBadgeIds = _currentStreak.badges.map((b) => b.id).toSet();

    // Insignias por racha
    if (streak >= 7 && !earnedBadgeIds.contains('streak_7')) {
      newBadges.add(AchievementBadge(
        id: 'streak_7',
        name: '7 Días de Racha',
        description: 'Mantuviste una racha de 7 días consecutivos',
        icon: '🔥',
        earnedDate: DateTime.now(),
      ));
    }

    if (streak >= 30 && !earnedBadgeIds.contains('streak_30')) {
      newBadges.add(AchievementBadge(
        id: 'streak_30',
        name: 'Racha de 1 Mes',
        description: 'Increíble! 30 días consecutivos activo',
        icon: '🏆',
        earnedDate: DateTime.now(),
      ));
    }

    // Insignias por aplicaciones
    if (activitiesCount >= 5 && !earnedBadgeIds.contains('first_apps')) {
      newBadges.add(AchievementBadge(
        id: 'first_apps',
        name: 'Primera Postulación',
        description: 'Aplicaste a tus primeros 5 trabajos',
        icon: '🚀',
        earnedDate: DateTime.now(),
      ));
    }

    // Insignias por puntos
    if (points >= 100 && !earnedBadgeIds.contains('points_100')) {
      newBadges.add(AchievementBadge(
        id: 'points_100',
        name: 'Centurión',
        description: 'Alcanzaste 100 puntos',
        icon: '⭐',
        earnedDate: DateTime.now(),
      ));
    }

    return newBadges;
  }

  // Obtener actividades recientes
  List<Activity> getRecentActivities({int limit = 10}) {
    return _currentStreak.activities.reversed.take(limit).toList();
  }

  // Resetear racha (para testing)
  void reset() {
    _currentStreak = Streak.initial();
  }
}
