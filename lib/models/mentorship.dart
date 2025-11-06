class MentorUser {
  final String id;
  final String name;
  final String email;
  final String? location;
  final List<String> skills;
  final String? experience;
  final int points;

  MentorUser({
    required this.id,
    required this.name,
    required this.email,
    this.location,
    required this.skills,
    this.experience,
    required this.points,
  });

  factory MentorUser.fromJson(Map<String, dynamic> json) {
    return MentorUser(
      id: json['id'].toString(),
      name: json['name'] ?? '',
      email: json['email'] ?? '',
      location: json['location'],
      skills: List<String>.from(json['skills'] ?? []),
      experience: json['experience'],
      points: json['points'] ?? 0,
    );
  }
}

class SuccessStory {
  final int id;
  final MentorUser user;
  final String company;
  final String position;
  final String hireDate;
  final String? salaryRange;
  final bool isWillingToMentor;
  final int maxMentees;
  final String successDescription;
  final List<String> keySkillsUsed;
  final int currentMenteesCount;
  final bool canAcceptMentees;
  final String statusDisplay;
  final String createdAt;

  SuccessStory({
    required this.id,
    required this.user,
    required this.company,
    required this.position,
    required this.hireDate,
    this.salaryRange,
    required this.isWillingToMentor,
    required this.maxMentees,
    required this.successDescription,
    required this.keySkillsUsed,
    required this.currentMenteesCount,
    required this.canAcceptMentees,
    required this.statusDisplay,
    required this.createdAt,
  });

  factory SuccessStory.fromJson(Map<String, dynamic> json) {
    return SuccessStory(
      id: json['id'],
      user: MentorUser.fromJson(json['user']),
      company: json['company'] ?? '',
      position: json['position'] ?? '',
      hireDate: json['hire_date'] ?? '',
      salaryRange: json['salary_range'],
      isWillingToMentor: json['is_willing_to_mentor'] ?? false,
      maxMentees: json['max_mentees'] ?? 3,
      successDescription: json['success_description'] ?? '',
      keySkillsUsed: List<String>.from(json['key_skills_used'] ?? []),
      currentMenteesCount: json['current_mentees_count'] ?? 0,
      canAcceptMentees: json['can_accept_mentees'] ?? false,
      statusDisplay: json['status_display'] ?? '',
      createdAt: json['created_at'] ?? '',
    );
  }

  String get salaryDisplay {
    if (salaryRange == null) return 'No especificado';
    
    final salaryMap = {
      '0-30k': '\$0 - \$30,000',
      '30k-50k': '\$30,000 - \$50,000',
      '50k-70k': '\$50,000 - \$70,000',
      '70k-100k': '\$70,000 - \$100,000',
      '100k+': '\$100,000+',
    };
    
    return salaryMap[salaryRange] ?? salaryRange!;
  }
}

class ProfileMatch {
  final int id;
  final MentorUser matchedUser;
  final int similarityScore;
  final List<String> matchingSkills;
  final double skillOverlapPercentage;
  final bool sameLocation;
  final bool similarExperienceLevel;
  final SuccessStory? successStory;
  final String calculatedAt;

  ProfileMatch({
    required this.id,
    required this.matchedUser,
    required this.similarityScore,
    required this.matchingSkills,
    required this.skillOverlapPercentage,
    required this.sameLocation,
    required this.similarExperienceLevel,
    this.successStory,
    required this.calculatedAt,
  });

  factory ProfileMatch.fromJson(Map<String, dynamic> json) {
    return ProfileMatch(
      id: json['id'],
      matchedUser: MentorUser.fromJson(json['matched_user']),
      similarityScore: json['similarity_score'] ?? 0,
      matchingSkills: List<String>.from(json['matching_skills'] ?? []),
      skillOverlapPercentage: (json['skill_overlap_percentage'] ?? 0.0).toDouble(),
      sameLocation: json['same_location'] ?? false,
      similarExperienceLevel: json['similar_experience_level'] ?? false,
      successStory: json['success_story'] != null 
          ? SuccessStory.fromJson(json['success_story'])
          : null,
      calculatedAt: json['calculated_at'] ?? '',
    );
  }

  String get scoreColor {
    if (similarityScore >= 80) return 'green';
    if (similarityScore >= 60) return 'yellow';
    return 'gray';
  }
}

class MentorshipRequest {
  final int id;
  final MentorUser fromUser;
  final MentorUser toUser;
  final String status;
  final String statusDisplay;
  final String message;
  final String? responseMessage;
  final String? respondedAt;
  final String createdAt;
  final String updatedAt;

  MentorshipRequest({
    required this.id,
    required this.fromUser,
    required this.toUser,
    required this.status,
    required this.statusDisplay,
    required this.message,
    this.responseMessage,
    this.respondedAt,
    required this.createdAt,
    required this.updatedAt,
  });

  factory MentorshipRequest.fromJson(Map<String, dynamic> json) {
    return MentorshipRequest(
      id: json['id'],
      fromUser: MentorUser.fromJson(json['from_user']),
      toUser: MentorUser.fromJson(json['to_user']),
      status: json['status'] ?? '',
      statusDisplay: json['status_display'] ?? '',
      message: json['message'] ?? '',
      responseMessage: json['response_message'],
      respondedAt: json['responded_at'],
      createdAt: json['created_at'] ?? '',
      updatedAt: json['updated_at'] ?? '',
    );
  }

  bool get isPending => status == 'pending';
  bool get isAccepted => status == 'accepted';
  bool get isDeclined => status == 'declined';
  bool get isCancelled => status == 'cancelled';
}
