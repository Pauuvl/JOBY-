import 'package:flutter/material.dart';
import '../models/mentorship.dart';
import '../services/mentorship_service.dart';

class MentorshipScreen extends StatefulWidget {
  const MentorshipScreen({Key? key}) : super(key: key);

  @override
  State<MentorshipScreen> createState() => _MentorshipScreenState();
}

class _MentorshipScreenState extends State<MentorshipScreen> with SingleTickerProviderStateMixin {
  final MentorshipService _mentorshipService = MentorshipService();
  late TabController _tabController;
  
  List<ProfileMatch> _mentors = [];
  List<MentorshipRequest> _sentRequests = [];
  List<MentorshipRequest> _receivedRequests = [];
  
  bool _isLoading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
    _loadData();
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  Future<void> _loadData() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final mentors = await _mentorshipService.findMentors();
      final sent = await _mentorshipService.getMyRequests(type: 'sent');
      final received = await _mentorshipService.getMyRequests(type: 'received');
      
      if (mounted) {
        setState(() {
          _mentors = mentors;
          _sentRequests = sent;
          _receivedRequests = received;
          _isLoading = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _error = e.toString();
          _isLoading = false;
        });
      }
    }
  }

  void _showSendRequestDialog(ProfileMatch match) {
    final messageController = TextEditingController(
      text: 'Hola ${match.matchedUser.name}, me gustaría conectar contigo para recibir mentoría. '
            'Veo que trabajas en ${match.successStory?.company} y compartimos interés en ${match.matchingSkills.take(3).join(", ")}.'
    );

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Enviar Solicitud de Mentoría'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('A: ${match.matchedUser.name}',
                style: const TextStyle(fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            TextField(
              controller: messageController,
              maxLines: 5,
              decoration: const InputDecoration(
                labelText: 'Mensaje',
                border: OutlineInputBorder(),
                hintText: 'Preséntate y explica por qué quieres conectar',
              ),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancelar'),
          ),
          ElevatedButton(
            onPressed: () async {
              try {
                await _mentorshipService.sendRequest(
                  toUserId: match.matchedUser.id,
                  message: messageController.text,
                );
                if (mounted) {
                  Navigator.pop(context);
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Solicitud enviada')),
                  );
                  _loadData();
                }
              } catch (e) {
                if (mounted) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text(e.toString())),
                  );
                }
              }
            },
            child: const Text('Enviar'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Mentorías'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        bottom: TabBar(
          controller: _tabController,
          tabs: const [
            Tab(text: 'Mentores', icon: Icon(Icons.people)),
            Tab(text: 'Enviadas', icon: Icon(Icons.send)),
            Tab(text: 'Recibidas', icon: Icon(Icons.inbox)),
          ],
        ),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _error != null
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Icon(Icons.error_outline, size: 64, color: Colors.grey),
                      const SizedBox(height: 16),
                      Text(_error!),
                      const SizedBox(height: 16),
                      ElevatedButton(
                        onPressed: _loadData,
                        child: const Text('Reintentar'),
                      ),
                    ],
                  ),
                )
              : TabBarView(
                  controller: _tabController,
                  children: [
                    _buildMentorsTab(),
                    _buildSentRequestsTab(),
                    _buildReceivedRequestsTab(),
                  ],
                ),
    );
  }

  Widget _buildMentorsTab() {
    if (_mentors.isEmpty) {
      return const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('🎓', style: TextStyle(fontSize: 64)),
            SizedBox(height: 16),
            Text('No hay mentores disponibles',
                style: TextStyle(fontSize: 18)),
          ],
        ),
      );
    }

    return RefreshIndicator(
      onRefresh: _loadData,
      child: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: _mentors.length,
        itemBuilder: (context, index) {
          final match = _mentors[index];
          return _buildMentorCard(match);
        },
      ),
    );
  }

  Widget _buildMentorCard(ProfileMatch match) {
    final story = match.successStory;
    if (story == null) return const SizedBox.shrink();

    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header with match score
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: [Colors.green.shade50, Colors.green.shade100],
              ),
            ),
            child: Row(
              children: [
                CircleAvatar(
                  radius: 30,
                  backgroundColor: Colors.green,
                  child: Text(
                    match.matchedUser.name[0].toUpperCase(),
                    style: const TextStyle(
                      fontSize: 24,
                      color: Colors.white,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        match.matchedUser.name,
                        style: const TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      Text(
                        '${story.position} en ${story.company}',
                        style: TextStyle(
                          fontSize: 14,
                          color: Colors.grey[700],
                        ),
                      ),
                    ],
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  decoration: BoxDecoration(
                    color: Colors.green,
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(
                    '${match.similarityScore}% Match',
                    style: const TextStyle(
                      color: Colors.white,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ),
          ),

          Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Skills en común
                if (match.matchingSkills.isNotEmpty) ...[
                  const Text(
                    'Skills en común:',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 8),
                  Wrap(
                    spacing: 6,
                    runSpacing: 6,
                    children: match.matchingSkills.map((skill) {
                      return Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        decoration: BoxDecoration(
                          color: Colors.green.shade50,
                          borderRadius: BorderRadius.circular(4),
                        ),
                        child: Text(
                          skill,
                          style: TextStyle(
                            fontSize: 12,
                            color: Colors.green.shade900,
                          ),
                        ),
                      );
                    }).toList(),
                  ),
                  const SizedBox(height: 12),
                ],

                // Historia de éxito
                Text(
                  story.successDescription,
                  style: TextStyle(color: Colors.grey[700]),
                  maxLines: 3,
                  overflow: TextOverflow.ellipsis,
                ),
                const SizedBox(height: 12),

                // Info row
                Row(
                  children: [
                    Icon(Icons.location_on, size: 16, color: Colors.grey[600]),
                    const SizedBox(width: 4),
                    Text(
                      match.matchedUser.location ?? 'No especificado',
                      style: TextStyle(fontSize: 12, color: Colors.grey[600]),
                    ),
                    const SizedBox(width: 16),
                    Icon(Icons.people, size: 16, color: Colors.grey[600]),
                    const SizedBox(width: 4),
                    Text(
                      '${story.currentMenteesCount}/${story.maxMentees} mentorados',
                      style: TextStyle(fontSize: 12, color: Colors.grey[600]),
                    ),
                  ],
                ),
                const SizedBox(height: 12),

                // Botón conectar
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton.icon(
                    onPressed: story.canAcceptMentees
                        ? () => _showSendRequestDialog(match)
                        : null,
                    icon: const Icon(Icons.connect_without_contact),
                    label: Text(story.canAcceptMentees
                        ? 'Conectar'
                        : 'No disponible'),
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 12),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSentRequestsTab() {
    if (_sentRequests.isEmpty) {
      return const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('📤', style: TextStyle(fontSize: 64)),
            SizedBox(height: 16),
            Text('No has enviado solicitudes'),
          ],
        ),
      );
    }

    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: _sentRequests.length,
      itemBuilder: (context, index) {
        final request = _sentRequests[index];
        return _buildRequestCard(request, isSent: true);
      },
    );
  }

  Widget _buildReceivedRequestsTab() {
    if (_receivedRequests.isEmpty) {
      return const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('📥', style: TextStyle(fontSize: 64)),
            SizedBox(height: 16),
            Text('No has recibido solicitudes'),
          ],
        ),
      );
    }

    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: _receivedRequests.length,
      itemBuilder: (context, index) {
        final request = _receivedRequests[index];
        return _buildRequestCard(request, isSent: false);
      },
    );
  }

  Widget _buildRequestCard(MentorshipRequest request, {required bool isSent}) {
    final user = isSent ? request.toUser : request.fromUser;
    
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                CircleAvatar(
                  child: Text(user.name[0].toUpperCase()),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        user.name,
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                      Text(
                        request.statusDisplay,
                        style: TextStyle(
                          fontSize: 12,
                          color: request.isPending
                              ? Colors.orange
                              : request.isAccepted
                                  ? Colors.green
                                  : Colors.grey,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Text(
              request.message,
              style: TextStyle(color: Colors.grey[700]),
            ),
            if (request.responseMessage != null) ...[
              const SizedBox(height: 8),
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: Colors.grey.shade100,
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  'Respuesta: ${request.responseMessage}',
                  style: const TextStyle(fontSize: 12),
                ),
              ),
            ],
            if (request.isPending) ...[
              const SizedBox(height: 12),
              if (isSent)
                TextButton(
                  onPressed: () async {
                    try {
                      await _mentorshipService.cancelRequest(request.id);
                      _loadData();
                      if (mounted) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text('Solicitud cancelada')),
                        );
                      }
                    } catch (e) {
                      if (mounted) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(content: Text(e.toString())),
                        );
                      }
                    }
                  },
                  child: const Text('Cancelar solicitud'),
                )
              else
                Row(
                  children: [
                    Expanded(
                      child: ElevatedButton(
                        onPressed: () async {
                          try {
                            await _mentorshipService.respondToRequest(
                              requestId: request.id,
                              action: 'accept',
                              responseMessage: '¡Con gusto! Conectemos',
                            );
                            _loadData();
                            if (mounted) {
                              ScaffoldMessenger.of(context).showSnackBar(
                                const SnackBar(content: Text('Solicitud aceptada')),
                              );
                            }
                          } catch (e) {
                            if (mounted) {
                              ScaffoldMessenger.of(context).showSnackBar(
                                SnackBar(content: Text(e.toString())),
                              );
                            }
                          }
                        },
                        child: const Text('Aceptar'),
                      ),
                    ),
                    const SizedBox(width: 8),
                    Expanded(
                      child: OutlinedButton(
                        onPressed: () async {
                          try {
                            await _mentorshipService.respondToRequest(
                              requestId: request.id,
                              action: 'decline',
                            );
                            _loadData();
                            if (mounted) {
                              ScaffoldMessenger.of(context).showSnackBar(
                                const SnackBar(content: Text('Solicitud rechazada')),
                              );
                            }
                          } catch (e) {
                            if (mounted) {
                              ScaffoldMessenger.of(context).showSnackBar(
                                SnackBar(content: Text(e.toString())),
                              );
                            }
                          }
                        },
                        child: const Text('Rechazar'),
                      ),
                    ),
                  ],
                ),
            ],
          ],
        ),
      ),
    );
  }
}
