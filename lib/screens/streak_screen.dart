import 'package:flutter/material.dart';
import '../services/streak_service.dart';
import '../models/streak.dart';

class StreakScreen extends StatefulWidget {
  const StreakScreen({super.key});

  @override
  State<StreakScreen> createState() => _StreakScreenState();
}

class _StreakScreenState extends State<StreakScreen> {
  final _streakService = StreakService();

  @override
  Widget build(BuildContext context) {
    final streak = _streakService.currentStreak;

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

            // Estadísticas
            Row(
              children: [
                Expanded(
                  child: _buildStatCard(
                    'Puntos Totales',
                    '${streak.totalPoints}',
                    Icons.stars,
                    Colors.amber,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: _buildStatCard(
                    'Actividades',
                    '${streak.activities.length}',
                    Icons.trending_up,
                    Colors.blue,
                  ),
                ),
              ],
            ),

            const SizedBox(height: 24),

            // Insignias
            const Text(
              'Insignias Ganadas',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),
            if (streak.badges.isEmpty)
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Center(
                    child: Column(
                      children: const [
                        Icon(Icons.emoji_events, size: 48, color: Colors.grey),
                        SizedBox(height: 8),
                        Text(
                          '¡Aún no tienes insignias!',
                          style: TextStyle(color: Colors.grey),
                        ),
                        Text(
                          'Mantén tu racha para ganar insignias',
                          style: TextStyle(color: Colors.grey, fontSize: 12),
                        ),
                      ],
                    ),
                  ),
                ),
              )
            else
              GridView.builder(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 3,
                  crossAxisSpacing: 12,
                  mainAxisSpacing: 12,
                ),
                itemCount: streak.badges.length,
                itemBuilder: (context, index) {
                  final badge = streak.badges[index];
                  return _buildBadgeCard(badge);
                },
              ),

            const SizedBox(height: 24),

            // Actividades recientes
            const Text(
              'Actividades Recientes',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),
            if (streak.activities.isEmpty)
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
              ..._streakService.getRecentActivities().map(
                    (activity) => _buildActivityCard(activity),
                  ),

            const SizedBox(height: 24),

            // Botón de prueba (para demo)
            ElevatedButton.icon(
              onPressed: () {
                setState(() {
                  _streakService.recordActivity(
                    'daily_login',
                    'Ingreso diario a la aplicación',
                    points: 10,
                  );
                });
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(
                    content: Text('¡+10 puntos! Racha actualizada 🔥'),
                    backgroundColor: Colors.green,
                  ),
                );
              },
              icon: const Icon(Icons.add),
              label: const Text('Registrar Actividad (Demo)'),
              style: ElevatedButton.styleFrom(
                minimumSize: const Size(double.infinity, 50),
              ),
            ),
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

  Widget _buildBadgeCard(AchievementBadge badge) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(8),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              badge.icon,
              style: const TextStyle(fontSize: 36),
            ),
            const SizedBox(height: 4),
            Text(
              badge.name,
              style: const TextStyle(
                fontSize: 10,
                fontWeight: FontWeight.bold,
              ),
              textAlign: TextAlign.center,
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildActivityCard(Activity activity) {
    IconData icon;
    Color color;

    switch (activity.type) {
      case 'job_applied':
        icon = Icons.work;
        color = Colors.blue;
        break;
      case 'profile_updated':
        icon = Icons.person;
        color = Colors.green;
        break;
      case 'daily_login':
        icon = Icons.login;
        color = Colors.orange;
        break;
      case 'friend_referred':
        icon = Icons.group_add;
        color = Colors.purple;
        break;
      default:
        icon = Icons.check_circle;
        color = Colors.grey;
    }

    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: color.withOpacity(0.2),
          child: Icon(icon, color: color),
        ),
        title: Text(activity.description),
        subtitle: Text(
          _formatDate(activity.date),
          style: const TextStyle(fontSize: 12),
        ),
        trailing: Text(
          '+${activity.points} pts',
          style: const TextStyle(
            fontWeight: FontWeight.bold,
            color: Colors.green,
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
