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

class _StreakScreenState extends State<StreakScreen> with SingleTickerProviderStateMixin {
  final _streakService = StreakService();
  Streak? _streak;
  List<Achievement> _achievements = [];
  List<PointsHistory> _pointsHistory = [];
  List<Challenge> _availableChallenges = [];
  List<UserChallenge> _activeChallenges = [];
  bool _isLoading = true;
  String? _error;
  TabController? _challengeTabController;

  @override
  void initState() {
    super.initState();
    _challengeTabController = TabController(length: 3, vsync: this);
    _loadData();
  }

  @override
  void dispose() {
    _challengeTabController?.dispose();
    super.dispose();
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
      final availableChallenges = await _streakService.getAvailableChallenges();
      final activeChallenges = await _streakService.getActiveChallenges();

      setState(() {
        _streak = streak;
        _achievements = achievements;
        _pointsHistory = pointsHistory;
        _availableChallenges = availableChallenges;
        _activeChallenges = activeChallenges;
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

  Future<void> _startChallenge(String challengeId, String title) async {
    try {
      final result = await _streakService.startChallenge(challengeId);
      
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(result['message'] ?? '¡Reto iniciado!'),
            backgroundColor: Colors.green,
          ),
        );
      }

      await _loadData(); // Recargar datos
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

            // Sección de Retos
            const Text(
              '🎯 Retos',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),
            
            // Pestañas de retos
            TabBar(
              controller: _challengeTabController,
              labelColor: Colors.deepPurple,
              unselectedLabelColor: Colors.grey,
              indicatorColor: Colors.deepPurple,
              tabs: const [
                Tab(text: 'Disponibles'),
                Tab(text: 'Activos'),
                Tab(text: 'Completados'),
              ],
            ),
            const SizedBox(height: 12),
            
            // Contenido de pestañas
            SizedBox(
              height: 300,
              child: TabBarView(
                controller: _challengeTabController,
                children: [
                  // Retos disponibles
                  _buildAvailableChallenges(),
                  // Retos activos
                  _buildActiveChallenges(),
                  // Retos completados
                  _buildCompletedChallenges(),
                ],
              ),
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

  Widget _buildAvailableChallenges() {
    if (_availableChallenges.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: const [
            Icon(Icons.check_circle, size: 48, color: Colors.green),
            SizedBox(height: 8),
            Text('No hay retos disponibles', style: TextStyle(color: Colors.grey)),
            Text('¡Has completado todos los retos!', style: TextStyle(color: Colors.grey, fontSize: 12)),
          ],
        ),
      );
    }

    return ListView.builder(
      itemCount: _availableChallenges.length,
      itemBuilder: (context, index) {
        final challenge = _availableChallenges[index];
        return _buildChallengeCard(challenge);
      },
    );
  }

  Widget _buildActiveChallenges() {
    if (_activeChallenges.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: const [
            Icon(Icons.hourglass_empty, size: 48, color: Colors.grey),
            SizedBox(height: 8),
            Text('No tienes retos activos', style: TextStyle(color: Colors.grey)),
            Text('¡Inicia un reto desde la pestaña "Disponibles"!', style: TextStyle(color: Colors.grey, fontSize: 12)),
          ],
        ),
      );
    }

    return ListView.builder(
      itemCount: _activeChallenges.length,
      itemBuilder: (context, index) {
        final userChallenge = _activeChallenges[index];
        return _buildUserChallengeCard(userChallenge);
      },
    );
  }

  Widget _buildCompletedChallenges() {
    return FutureBuilder<List<UserChallenge>>(
      future: _streakService.getCompletedChallenges(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Center(child: CircularProgressIndicator());
        }

        if (snapshot.hasError) {
          return Center(child: Text('Error: ${snapshot.error}'));
        }

        final completedChallenges = snapshot.data ?? [];

        if (completedChallenges.isEmpty) {
          return Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: const [
                Icon(Icons.task_alt, size: 48, color: Colors.grey),
                SizedBox(height: 8),
                Text('Aún no has completado retos', style: TextStyle(color: Colors.grey)),
              ],
            ),
          );
        }

        return ListView.builder(
          itemCount: completedChallenges.length,
          itemBuilder: (context, index) {
            final userChallenge = completedChallenges[index];
            return _buildUserChallengeCard(userChallenge);
          },
        );
      },
    );
  }

  Widget _buildChallengeCard(Challenge challenge) {
    Color typeColor = Colors.grey;
    if (challenge.challengeType == 'daily') typeColor = Colors.blue;
    if (challenge.challengeType == 'weekly') typeColor = Colors.purple;
    if (challenge.challengeType == 'special') typeColor = Colors.orange;

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Text(challenge.icon, style: const TextStyle(fontSize: 32)),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        challenge.title,
                        style: const TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                        decoration: BoxDecoration(
                          color: typeColor.withOpacity(0.2),
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Text(
                          challenge.typeDisplay,
                          style: TextStyle(
                            fontSize: 12,
                            color: typeColor,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                Column(
                  children: [
                    const Icon(Icons.stars, color: Colors.amber, size: 20),
                    Text(
                      '+${challenge.pointsReward}',
                      style: const TextStyle(
                        fontWeight: FontWeight.bold,
                        color: Colors.amber,
                      ),
                    ),
                  ],
                ),
              ],
            ),
            const SizedBox(height: 12),
            Text(
              challenge.description,
              style: const TextStyle(color: Colors.grey),
            ),
            const SizedBox(height: 12),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: () => _startChallenge(challenge.id, challenge.title),
                style: ElevatedButton.styleFrom(
                  backgroundColor: typeColor,
                  foregroundColor: Colors.white,
                ),
                child: const Text('Iniciar Reto'),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildUserChallengeCard(UserChallenge userChallenge) {
    final challenge = userChallenge.challengeDetails;
    if (challenge == null) return const SizedBox();

    Color statusColor = Colors.blue;
    if (userChallenge.status == 'completed') statusColor = Colors.green;
    if (userChallenge.status == 'failed' || userChallenge.status == 'expired') statusColor = Colors.red;

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Text(challenge.icon, style: const TextStyle(fontSize: 32)),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        challenge.title,
                        style: const TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        userChallenge.statusDisplay,
                        style: TextStyle(
                          fontSize: 12,
                          color: statusColor,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                ),
                if (userChallenge.isCompleted && userChallenge.pointsEarned != null)
                  Column(
                    children: [
                      const Icon(Icons.check_circle, color: Colors.green, size: 20),
                      Text(
                        '+${userChallenge.pointsEarned}',
                        style: const TextStyle(
                          fontWeight: FontWeight.bold,
                          color: Colors.green,
                        ),
                      ),
                    ],
                  ),
              ],
            ),
            const SizedBox(height: 12),
            Text(
              challenge.description,
              style: const TextStyle(color: Colors.grey, fontSize: 12),
            ),
            const SizedBox(height: 12),
            // Barra de progreso
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      '${userChallenge.currentProgress} / ${userChallenge.targetCount}',
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                    Text(
                      '${userChallenge.progressPercentage.toInt()}%',
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                LinearProgressIndicator(
                  value: userChallenge.progressPercentage / 100,
                  backgroundColor: Colors.grey[300],
                  valueColor: AlwaysStoppedAnimation<Color>(statusColor),
                  minHeight: 8,
                ),
              ],
            ),
            if (userChallenge.expiresAt != null && userChallenge.status == 'active')
              Padding(
                padding: const EdgeInsets.only(top: 8),
                child: Row(
                  children: [
                    const Icon(Icons.access_time, size: 14, color: Colors.orange),
                    const SizedBox(width: 4),
                    Text(
                      'Expira: ${_formatDateTime(userChallenge.expiresAt!)}',
                      style: const TextStyle(fontSize: 12, color: Colors.orange),
                    ),
                  ],
                ),
              ),
          ],
        ),
      ),
    );
  }

  String _formatDateTime(DateTime date) {
    final now = DateTime.now();
    final difference = now.difference(date);

    if (difference.isNegative) {
      final futureTime = date.difference(now);
      if (futureTime.inHours < 24) {
        return 'en ${futureTime.inHours} horas';
      } else {
        return 'en ${futureTime.inDays} días';
      }
    }

    if (difference.inMinutes < 60) {
      return 'Hace ${difference.inMinutes} minutos';
    } else if (difference.inHours < 24) {
      return 'Hace ${difference.inHours} horas';
    } else {
      return 'Hace ${difference.inDays} días';
    }
  }
}
