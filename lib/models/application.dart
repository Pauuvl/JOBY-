import 'job.dart';

class Application {
  final String id;
  final Job? job;
  final String? jobId;
  final String coverLetter;
  final String? resume;
  final String? portfolioUrl;
  final String status; // 'pending', 'reviewed', 'interview', 'offered', 'accepted', 'rejected', 'withdrawn'
  final String? statusNotes;
  final DateTime appliedAt;
  final DateTime? reviewedAt;
  final DateTime? interviewScheduledAt;
  final String? interviewLocation;
  final String? interviewNotes;

  Application({
    required this.id,
    this.job,
    this.jobId,
    required this.coverLetter,
    this.resume,
    this.portfolioUrl,
    required this.status,
    this.statusNotes,
    required this.appliedAt,
    this.reviewedAt,
    this.interviewScheduledAt,
    this.interviewLocation,
    this.interviewNotes,
  });

  factory Application.fromJson(Map<String, dynamic> json) {
    return Application(
      id: json['id'],
      job: json['job_details'] != null ? Job.fromJson(json['job_details']) : null,
      jobId: json['job'],
      coverLetter: json['cover_letter'] ?? '',
      resume: json['resume'],
      portfolioUrl: json['portfolio_url'],
      status: json['status'],
      statusNotes: json['status_notes'],
      appliedAt: DateTime.parse(json['applied_at']),
      reviewedAt: json['reviewed_at'] != null 
          ? DateTime.parse(json['reviewed_at']) 
          : null,
      interviewScheduledAt: json['interview_scheduled_at'] != null 
          ? DateTime.parse(json['interview_scheduled_at']) 
          : null,
      interviewLocation: json['interview_location'],
      interviewNotes: json['interview_notes'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'job': jobId,
      'cover_letter': coverLetter,
      'resume': resume,
      'portfolio_url': portfolioUrl,
      'status': status,
      'status_notes': statusNotes,
      'applied_at': appliedAt.toIso8601String(),
      'reviewed_at': reviewedAt?.toIso8601String(),
      'interview_scheduled_at': interviewScheduledAt?.toIso8601String(),
      'interview_location': interviewLocation,
      'interview_notes': interviewNotes,
    };
  }

  String get statusDisplay {
    switch (status) {
      case 'pending':
        return 'Pendiente';
      case 'reviewed':
        return 'Revisada';
      case 'interview':
        return 'Entrevista';
      case 'offered':
        return 'Oferta recibida';
      case 'accepted':
        return 'Aceptada';
      case 'rejected':
        return 'Rechazada';
      case 'withdrawn':
        return 'Retirada';
      default:
        return status;
    }
  }

  bool get isActive {
    return !['accepted', 'rejected', 'withdrawn'].contains(status);
  }

  Application copyWith({
    String? id,
    Job? job,
    String? jobId,
    String? coverLetter,
    String? resume,
    String? portfolioUrl,
    String? status,
    String? statusNotes,
    DateTime? appliedAt,
    DateTime? reviewedAt,
    DateTime? interviewScheduledAt,
    String? interviewLocation,
    String? interviewNotes,
  }) {
    return Application(
      id: id ?? this.id,
      job: job ?? this.job,
      jobId: jobId ?? this.jobId,
      coverLetter: coverLetter ?? this.coverLetter,
      resume: resume ?? this.resume,
      portfolioUrl: portfolioUrl ?? this.portfolioUrl,
      status: status ?? this.status,
      statusNotes: statusNotes ?? this.statusNotes,
      appliedAt: appliedAt ?? this.appliedAt,
      reviewedAt: reviewedAt ?? this.reviewedAt,
      interviewScheduledAt: interviewScheduledAt ?? this.interviewScheduledAt,
      interviewLocation: interviewLocation ?? this.interviewLocation,
      interviewNotes: interviewNotes ?? this.interviewNotes,
    );
  }
}
