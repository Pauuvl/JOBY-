import 'package:flutter/material.dart';
import '../models/challenge.dart';
import '../services/challenge_service.dart';

class CompletedChallengesScreen extends StatefulWidget {
  const CompletedChallengesScreen({Key? key}) : super(key: key);

  @override
  State<CompletedChallengesScreen> createState() => _CompletedChallengesScreenState();
}

class _CompletedChallengesScreenState extends State<CompletedChallengesScreen> {
  final ChallengeService _challengeService = ChallengeService();
  List<UserChallenge> _challenges = [];
  bool _isLoading = true;
  String? _error;
  String _selectedCategory = 'all';

  final Map<String, String> _categories = {
    'all': 'Todos',
    'applications': 'Aplicaciones',
    'profile': 'Perfil',
    'learning': 'Aprendizaje',
    'networking': 'Networking',
    'streak': 'Racha',
    'exploration': 'Exploración',
  };

  @override
  void initState() {
    super.initState();
    _loadChallenges();
  }

  Future<void> _loadChallenges() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final challenges = await _challengeService.getCompletedChallenges();
      if (mounted) {
        setState(() {
          _challenges = challenges;
          _isLoading = false;
        });
      }
    } catch (e) {
      print('Error loading challenges: $e');
      if (mounted) {
        setState(() {
          _error = 'Error al cargar retos completados';
          _isLoading = false;
        });
      }
    }
  }

  List<UserChallenge> get _filteredChallenges {
    if (_selectedCategory == 'all') {
      return _challenges;
    }
    return _challenges.where((c) => c.challenge.category == _selectedCategory).toList();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Retos Completados'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: Column(
        children: [
          // Category filter
          Container(
            height: 50,
            color: Colors.grey[100],
            child: ListView.builder(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.symmetric(horizontal: 8),
              itemCount: _categories.length,
              itemBuilder: (context, index) {
                final category = _categories.keys.elementAt(index);
                final label = _categories[category]!;
                final isSelected = _selectedCategory == category;

                return Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 4),
                  child: ChoiceChip(
                    label: Text(label),
                    selected: isSelected,
                    onSelected: (selected) {
                      if (selected) {
                        setState(() {
                          _selectedCategory = category;
                        });
                      }
                    },
                  ),
                );
              },
            ),
          ),

          // Stats summary
          if (!_isLoading && _challenges.isNotEmpty)
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: [Colors.purple.shade400, Colors.deepPurple.shade600],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  _buildStatItem(
                    '${_challenges.length}',
                    'Retos\nCompletados',
                    Icons.emoji_events,
                  ),
                  _buildStatItem(
                    '${_challenges.fold<int>(0, (sum, c) => sum + c.pointsEarned)}',
                    'Puntos\nGanados',
                    Icons.stars,
                  ),
                  _buildStatItem(
                    '${_challenges.where((c) => c.challenge.challengeType == 'daily').length}',
                    'Retos\nDiarios',
                    Icons.calendar_today,
                  ),
                ],
              ),
            ),

          // Challenges list
          Expanded(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator())
                : _error != null
                    ? Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(Icons.error_outline, size: 64, color: Colors.grey),
                            const SizedBox(height: 16),
                            Text(_error!),
                            const SizedBox(height: 16),
                            ElevatedButton(
                              onPressed: _loadChallenges,
                              child: const Text('Reintentar'),
                            ),
                          ],
                        ),
                      )
                    : _filteredChallenges.isEmpty
                        ? Center(
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Text(
                                  '🏆',
                                  style: TextStyle(fontSize: 64),
                                ),
                                const SizedBox(height: 16),
                                Text(
                                  'No hay retos completados',
                                  style: TextStyle(
                                    fontSize: 18,
                                    color: Colors.grey[600],
                                  ),
                                ),
                                const SizedBox(height: 8),
                                Text(
                                  '¡Completa retos para ganar puntos!',
                                  style: TextStyle(color: Colors.grey),
                                ),
                              ],
                            ),
                          )
                        : RefreshIndicator(
                            onRefresh: _loadChallenges,
                            child: ListView.builder(
                              padding: const EdgeInsets.all(16),
                              itemCount: _filteredChallenges.length,
                              itemBuilder: (context, index) {
                                final userChallenge = _filteredChallenges[index];
                                return _buildChallengeCard(userChallenge);
                              },
                            ),
                          ),
          ),
        ],
      ),
    );
  }

  Widget _buildStatItem(String value, String label, IconData icon) {
    return Column(
      children: [
        Icon(icon, color: Colors.white, size: 32),
        const SizedBox(height: 8),
        Text(
          value,
          style: const TextStyle(
            color: Colors.white,
            fontSize: 24,
            fontWeight: FontWeight.bold,
          ),
        ),
        Text(
          label,
          textAlign: TextAlign.center,
          style: const TextStyle(
            color: Colors.white70,
            fontSize: 12,
          ),
        ),
      ],
    );
  }

  Widget _buildChallengeCard(UserChallenge userChallenge) {
    final challenge = userChallenge.challenge;
    
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                // Icon
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.green.shade50,
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Text(
                    challenge.icon,
                    style: const TextStyle(fontSize: 32),
                  ),
                ),
                const SizedBox(width: 16),
                
                // Title and category
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
                      Row(
                        children: [
                          Container(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 8,
                              vertical: 2,
                            ),
                            decoration: BoxDecoration(
                              color: Colors.blue.shade100,
                              borderRadius: BorderRadius.circular(4),
                            ),
                            child: Text(
                              challenge.categoryDisplay,
                              style: TextStyle(
                                fontSize: 12,
                                color: Colors.blue.shade900,
                              ),
                            ),
                          ),
                          const SizedBox(width: 8),
                          Text(
                            challenge.typeDisplay,
                            style: TextStyle(
                              fontSize: 12,
                              color: Colors.grey[600],
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
                
                // Points earned
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 12,
                    vertical: 6,
                  ),
                  decoration: BoxDecoration(
                    color: Colors.amber.shade100,
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.stars, color: Colors.amber, size: 16),
                      const SizedBox(width: 4),
                      Text(
                        '+${userChallenge.pointsEarned}',
                        style: TextStyle(
                          color: Colors.amber.shade900,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            
            const SizedBox(height: 12),
            
            // Description
            Text(
              challenge.description,
              style: TextStyle(
                color: Colors.grey[700],
                fontSize: 14,
              ),
            ),
            
            const SizedBox(height: 12),
            
            // Completion info
            Row(
              children: [
                Icon(Icons.check_circle, color: Colors.green, size: 16),
                const SizedBox(width: 4),
                Text(
                  'Completado ${userChallenge.timeAgo}',
                  style: TextStyle(
                    color: Colors.grey[600],
                    fontSize: 12,
                  ),
                ),
                const Spacer(),
                Text(
                  '${userChallenge.currentProgress}/${challenge.targetCount}',
                  style: TextStyle(
                    color: Colors.grey[600],
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
