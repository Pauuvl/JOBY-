class AppNotification {
  final String id;
  final String notificationType;
  final String title;
  final String message;
  final Map<String, dynamic>? data;
  final String? actionUrl;
  final bool isRead;
  final DateTime? readAt;
  final DateTime createdAt;

  AppNotification({
    required this.id,
    required this.notificationType,
    required this.title,
    required this.message,
    this.data,
    this.actionUrl,
    this.isRead = false,
    this.readAt,
    required this.createdAt,
  });

  factory AppNotification.fromJson(Map<String, dynamic> json) {
    return AppNotification(
      id: json['id'],
      notificationType: json['notification_type'],
      title: json['title'],
      message: json['message'],
      data: json['data'],
      actionUrl: json['action_url'],
      isRead: json['is_read'] ?? false,
      readAt: json['read_at'] != null 
          ? DateTime.parse(json['read_at']) 
          : null,
      createdAt: DateTime.parse(json['created_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'notification_type': notificationType,
      'title': title,
      'message': message,
      'data': data,
      'action_url': actionUrl,
      'is_read': isRead,
      'read_at': readAt?.toIso8601String(),
      'created_at': createdAt.toIso8601String(),
    };
  }

  String get typeDisplay {
    switch (notificationType) {
      case 'application_status':
        return 'Estado de aplicación';
      case 'new_job':
        return 'Nuevo empleo';
      case 'achievement':
        return 'Logro';
      case 'streak':
        return 'Racha';
      case 'message':
        return 'Mensaje';
      case 'reminder':
        return 'Recordatorio';
      case 'system':
        return 'Sistema';
      default:
        return notificationType;
    }
  }

  AppNotification copyWith({
    String? id,
    String? notificationType,
    String? title,
    String? message,
    Map<String, dynamic>? data,
    String? actionUrl,
    bool? isRead,
    DateTime? readAt,
    DateTime? createdAt,
  }) {
    return AppNotification(
      id: id ?? this.id,
      notificationType: notificationType ?? this.notificationType,
      title: title ?? this.title,
      message: message ?? this.message,
      data: data ?? this.data,
      actionUrl: actionUrl ?? this.actionUrl,
      isRead: isRead ?? this.isRead,
      readAt: readAt ?? this.readAt,
      createdAt: createdAt ?? this.createdAt,
    );
  }
}

class NotificationPreference {
  final String id;
  final bool emailApplicationStatus;
  final bool pushApplicationStatus;
  final bool inappApplicationStatus;
  final bool emailNewJob;
  final bool pushNewJob;
  final bool inappNewJob;
  final bool emailAchievement;
  final bool pushAchievement;
  final bool inappAchievement;
  final bool emailStreak;
  final bool pushStreak;
  final bool inappStreak;
  final bool emailMessage;
  final bool pushMessage;
  final bool inappMessage;
  final bool emailReminder;
  final bool pushReminder;
  final bool inappReminder;
  final bool emailSystem;
  final bool pushSystem;
  final bool inappSystem;

  NotificationPreference({
    required this.id,
    this.emailApplicationStatus = true,
    this.pushApplicationStatus = true,
    this.inappApplicationStatus = true,
    this.emailNewJob = true,
    this.pushNewJob = true,
    this.inappNewJob = true,
    this.emailAchievement = true,
    this.pushAchievement = true,
    this.inappAchievement = true,
    this.emailStreak = false,
    this.pushStreak = true,
    this.inappStreak = true,
    this.emailMessage = true,
    this.pushMessage = true,
    this.inappMessage = true,
    this.emailReminder = true,
    this.pushReminder = true,
    this.inappReminder = true,
    this.emailSystem = true,
    this.pushSystem = true,
    this.inappSystem = true,
  });

  factory NotificationPreference.fromJson(Map<String, dynamic> json) {
    return NotificationPreference(
      id: json['id'],
      emailApplicationStatus: json['email_application_status'] ?? true,
      pushApplicationStatus: json['push_application_status'] ?? true,
      inappApplicationStatus: json['inapp_application_status'] ?? true,
      emailNewJob: json['email_new_job'] ?? true,
      pushNewJob: json['push_new_job'] ?? true,
      inappNewJob: json['inapp_new_job'] ?? true,
      emailAchievement: json['email_achievement'] ?? true,
      pushAchievement: json['push_achievement'] ?? true,
      inappAchievement: json['inapp_achievement'] ?? true,
      emailStreak: json['email_streak'] ?? false,
      pushStreak: json['push_streak'] ?? true,
      inappStreak: json['inapp_streak'] ?? true,
      emailMessage: json['email_message'] ?? true,
      pushMessage: json['push_message'] ?? true,
      inappMessage: json['inapp_message'] ?? true,
      emailReminder: json['email_reminder'] ?? true,
      pushReminder: json['push_reminder'] ?? true,
      inappReminder: json['inapp_reminder'] ?? true,
      emailSystem: json['email_system'] ?? true,
      pushSystem: json['push_system'] ?? true,
      inappSystem: json['inapp_system'] ?? true,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'email_application_status': emailApplicationStatus,
      'push_application_status': pushApplicationStatus,
      'inapp_application_status': inappApplicationStatus,
      'email_new_job': emailNewJob,
      'push_new_job': pushNewJob,
      'inapp_new_job': inappNewJob,
      'email_achievement': emailAchievement,
      'push_achievement': pushAchievement,
      'inapp_achievement': inappAchievement,
      'email_streak': emailStreak,
      'push_streak': pushStreak,
      'inapp_streak': inappStreak,
      'email_message': emailMessage,
      'push_message': pushMessage,
      'inapp_message': inappMessage,
      'email_reminder': emailReminder,
      'push_reminder': pushReminder,
      'inapp_reminder': inappReminder,
      'email_system': emailSystem,
      'push_system': pushSystem,
      'inapp_system': inappSystem,
    };
  }
}
