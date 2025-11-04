import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/streak_service_real.dart';
import '../models/streak.dart';
import '../providers/auth_provider.dart';

class StreakScreen extends StatefulWidget {
  const StreakScreen({super.key});

  @override
  State<StreakScreen> createState() => _StreakScreenState();
}

class _StreakScreenState extends State<StreakScreen> {
  final _streakService = StreakService();
  Streak? _streak;
  List<Achievement> _achievements = [];
  List<PointsHistory> _pointsHistory = [];
  bool _isLoading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final streak = await _streakService.getMyStreak();
      final achievements = await _streakService.getMyAchievements();
      final pointsHistory = await _streakService.getPointsHistory();

      setState(() {
        _streak = streak;
        _achievements = achievements;
        _pointsHistory = pointsHistory;
        _isLoading = false;
      });
    } catch (e, stackTrace) {
      print('ERROR en StreakScreen: $e');
      print('StackTrace: $stackTrace');
      setState(() {
        _error = 'Error al cargar datos:\n$e';
        _isLoading = false;
      });
    }
  }

  Future<void> _recordActivity() async {
    try {
      final updatedStreak = await _streakService.recordActivity();
      final authProvider = context.read<AuthProvider>();
      await authProvider.refreshUser(); // Actualizar puntos del usuario

      setState(() {
        _streak = updatedStreak;
      });

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('¡+5 puntos! Actividad registrada 🔥'),
            backgroundColor: Colors.green,
          ),
        );
      }

      await _loadData(); // Recargar todo
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return Scaffold(
        appBar: AppBar(
          title: const Text('Mis Rachas'),
        ),
        body: const Center(child: CircularProgressIndicator()),
      );
    }

    if (_error != null) {
      return Scaffold(
        appBar: AppBar(
          title: const Text('Mis Rachas'),
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.error_outline, size: 64, color: Colors.red),
              const SizedBox(height: 16),
              Text(_error!),
              const SizedBox(height: 16),
              ElevatedButton(
                onPressed: _loadData,
                child: const Text('Reintentar'),
              ),
            ],
          ),
        ),
      );
    }

    final streak = _streak!;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Mis Rachas'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Tarjeta de racha principal
            Card(
              elevation: 4,
              child: Container(
                width: double.infinity,
                padding: const EdgeInsets.all(24),
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    colors: [Colors.orange.shade400, Colors.red.shade400],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Column(
                  children: [
                    const Text(
                      '🔥',
                      style: TextStyle(fontSize: 64),
                    ),
                    const SizedBox(height: 16),
                    const Text(
                      'Racha Actual',
                      style: TextStyle(
                        fontSize: 18,
                        color: Colors.white70,
                      ),
                    ),
                    Text(
                      '${streak.currentStreak} días',
                      style: const TextStyle(
                        fontSize: 48,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'Récord: ${streak.longestStreak} días',
                      style: const TextStyle(
                        fontSize: 16,
                        color: Colors.white70,
                      ),
                    ),
                  ],
                ),
              ),
            ),

            const SizedBox(height: 24),

            // Botón para registrar actividad diaria
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: _recordActivity,
                icon: const Icon(Icons.add_circle_outline),
                label: const Text('Registrar Actividad Diaria (+5 puntos)'),
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.all(16),
                ),
              ),
            ),

            const SizedBox(height: 24),

            // Estadísticas
            Row(
              children: [
                Expanded(
                  child: _buildStatCard(
                    'Inicios',
                    '${streak.totalLogins}',
                    Icons.login,
                    Colors.blue,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: _buildStatCard(
                    'Aplicaciones',
                    '${streak.totalApplications}',
                    Icons.work,
                    Colors.green,
                  ),
                ),
              ],
            ),

            const SizedBox(height: 24),

            // Logros obtenidos
            const Text(
              'Mis Logros',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),
            if (_achievements.isEmpty)
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Center(
                    child: Column(
                      children: const [
                        Icon(Icons.emoji_events, size: 48, color: Colors.grey),
                        SizedBox(height: 8),
                        Text(
                          '¡Aún no tienes logros!',
                          style: TextStyle(color: Colors.grey),
                        ),
                        Text(
                          'Completa actividades para desbloquear logros',
                          style: TextStyle(color: Colors.grey, fontSize: 12),
                        ),
                      ],
                    ),
                  ),
                ),
              )
            else
              ListView.builder(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                itemCount: _achievements.length,
                itemBuilder: (context, index) {
                  final achievement = _achievements[index];
                  return _buildAchievementCard(achievement);
                },
              ),

            const SizedBox(height: 24),

            // Historial de puntos
            const Text(
              'Historial de Puntos',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),
            if (_pointsHistory.isEmpty)
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Center(
                    child: Column(
                      children: const [
                        Icon(Icons.history, size: 48, color: Colors.grey),
                        SizedBox(height: 8),
                        Text(
                          'No hay actividades aún',
                          style: TextStyle(color: Colors.grey),
                        ),
                      ],
                    ),
                  ),
                ),
              )
            else
              ListView.builder(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                itemCount: _pointsHistory.length,
                itemBuilder: (context, index) {
                  final history = _pointsHistory[index];
                  return _buildPointsHistoryCard(history);
                },
              ),

            const SizedBox(height: 24),
          ],
        ),
      ),
    );
  }

  Widget _buildStatCard(String label, String value, IconData icon, Color color) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Icon(icon, size: 32, color: color),
            const SizedBox(height: 8),
            Text(
              value,
              style: const TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
            Text(
              label,
              style: const TextStyle(
                fontSize: 12,
                color: Colors.grey,
              ),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildAchievementCard(Achievement achievement) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: ListTile(
        leading: Container(
          width: 50,
          height: 50,
          decoration: BoxDecoration(
            color: Colors.amber.shade100,
            borderRadius: BorderRadius.circular(25),
          ),
          child: Center(
            child: Text(
              achievement.icon,
              style: const TextStyle(fontSize: 24),
            ),
          ),
        ),
        title: Text(
          achievement.name,
          style: const TextStyle(fontWeight: FontWeight.bold),
        ),
        subtitle: Text(achievement.description),
        trailing: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.stars, color: Colors.amber, size: 20),
            Text(
              '+${achievement.pointsReward}',
              style: const TextStyle(
                fontWeight: FontWeight.bold,
                color: Colors.amber,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildPointsHistoryCard(PointsHistory history) {
    IconData icon;
    Color color;

    switch (history.action) {
      case 'daily_login':
        icon = Icons.login;
        color = Colors.blue;
        break;
      case 'job_application':
        icon = Icons.work;
        color = Colors.green;
        break;
      case 'profile_update':
        icon = Icons.person;
        color = Colors.orange;
        break;
      case 'achievement_earned':
        icon = Icons.emoji_events;
        color = Colors.amber;
        break;
      default:
        icon = Icons.add_circle;
        color = Colors.grey;
    }

    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: color.withOpacity(0.2),
          child: Icon(icon, color: color),
        ),
        title: Text(history.actionDisplay),
        subtitle: Text(
          history.description ?? '',
          style: const TextStyle(fontSize: 12),
        ),
        trailing: Text(
          '${history.points >= 0 ? '+' : ''}${history.points} pts',
          style: TextStyle(
            fontWeight: FontWeight.bold,
            color: history.points >= 0 ? Colors.green : Colors.red,
          ),
        ),
      ),
    );
  }

  String _formatDate(DateTime date) {
    final now = DateTime.now();
    final difference = now.difference(date);

    if (difference.inMinutes < 60) {
      return 'Hace ${difference.inMinutes} minutos';
    } else if (difference.inHours < 24) {
      return 'Hace ${difference.inHours} horas';
    } else {
      return 'Hace ${difference.inDays} días';
    }
  }
}
