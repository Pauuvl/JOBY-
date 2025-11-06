class ReferralCode {
  final String id;
  final String code;
  final int totalReferrals;
  final int totalPointsEarned;
  final bool isActive;
  final DateTime createdAt;
  final String shareLink;
  final String shareMessage;

  ReferralCode({
    required this.id,
    required this.code,
    required this.totalReferrals,
    required this.totalPointsEarned,
    required this.isActive,
    required this.createdAt,
    required this.shareLink,
    required this.shareMessage,
  });

  factory ReferralCode.fromJson(Map<String, dynamic> json) {
    return ReferralCode(
      id: json['id'].toString(),
      code: json['code'],
      totalReferrals: json['total_referrals'],
      totalPointsEarned: json['total_points_earned'],
      isActive: json['is_active'],
      createdAt: DateTime.parse(json['created_at']),
      shareLink: json['share_link'],
      shareMessage: json['share_message'],
    );
  }
}

class ReferredUser {
  final String id;
  final String name;
  final String email;
  final DateTime createdAt;

  ReferredUser({
    required this.id,
    required this.name,
    required this.email,
    required this.createdAt,
  });

  factory ReferredUser.fromJson(Map<String, dynamic> json) {
    return ReferredUser(
      id: json['id'],
      name: json['name'],
      email: json['email'],
      createdAt: DateTime.parse(json['created_at']),
    );
  }
}

class Referral {
  final int id;
  final ReferredUser referred;
  final String status;
  final String statusDisplay;
  final bool registrationPointsAwarded;
  final bool profileCompletionPointsAwarded;
  final bool employmentPointsAwarded;
  final DateTime referredAt;
  final DateTime lastMilestoneAt;

  Referral({
    required this.id,
    required this.referred,
    required this.status,
    required this.statusDisplay,
    required this.registrationPointsAwarded,
    required this.profileCompletionPointsAwarded,
    required this.employmentPointsAwarded,
    required this.referredAt,
    required this.lastMilestoneAt,
  });

  factory Referral.fromJson(Map<String, dynamic> json) {
    return Referral(
      id: json['id'],
      referred: ReferredUser.fromJson(json['referred']),
      status: json['status'],
      statusDisplay: json['status_display'],
      registrationPointsAwarded: json['registration_points_awarded'],
      profileCompletionPointsAwarded: json['profile_completion_points_awarded'],
      employmentPointsAwarded: json['employment_points_awarded'],
      referredAt: DateTime.parse(json['referred_at']),
      lastMilestoneAt: DateTime.parse(json['last_milestone_at']),
    );
  }

  String get statusEmoji {
    switch (status) {
      case 'registered':
        return '✅';
      case 'profile_completed':
        return '🌟';
      case 'employed':
        return '🎉';
      default:
        return '⏳';
    }
  }
}

class PointsTransaction {
  final int id;
  final String transactionType;
  final String transactionTypeDisplay;
  final int points;
  final String description;
  final String? relatedUserName;
  final DateTime createdAt;

  PointsTransaction({
    required this.id,
    required this.transactionType,
    required this.transactionTypeDisplay,
    required this.points,
    required this.description,
    this.relatedUserName,
    required this.createdAt,
  });

  factory PointsTransaction.fromJson(Map<String, dynamic> json) {
    return PointsTransaction(
      id: json['id'],
      transactionType: json['transaction_type'],
      transactionTypeDisplay: json['transaction_type_display'],
      points: json['points'],
      description: json['description'],
      relatedUserName: json['related_user_name'],
      createdAt: DateTime.parse(json['created_at']),
    );
  }

  bool get isPositive => points > 0;
}

class Reward {
  final int id;
  final String name;
  final String description;
  final String rewardType;
  final String rewardTypeDisplay;
  final int pointsRequired;
  final String icon;
  final bool isActive;
  final int maxRedemptionsPerUser;
  final int? totalAvailable;
  final bool canRedeem;
  final int timesRedeemed;

  Reward({
    required this.id,
    required this.name,
    required this.description,
    required this.rewardType,
    required this.rewardTypeDisplay,
    required this.pointsRequired,
    required this.icon,
    required this.isActive,
    required this.maxRedemptionsPerUser,
    this.totalAvailable,
    required this.canRedeem,
    required this.timesRedeemed,
  });

  factory Reward.fromJson(Map<String, dynamic> json) {
    return Reward(
      id: json['id'],
      name: json['name'],
      description: json['description'],
      rewardType: json['reward_type'],
      rewardTypeDisplay: json['reward_type_display'],
      pointsRequired: json['points_required'],
      icon: json['icon'],
      isActive: json['is_active'],
      maxRedemptionsPerUser: json['max_redemptions_per_user'],
      totalAvailable: json['total_available'],
      canRedeem: json['can_redeem'],
      timesRedeemed: json['times_redeemed'],
    );
  }

  bool get hasRedemptionsLeft => timesRedeemed < maxRedemptionsPerUser;
}

class RewardRedemption {
  final int id;
  final Reward reward;
  final int pointsSpent;
  final DateTime redeemedAt;

  RewardRedemption({
    required this.id,
    required this.reward,
    required this.pointsSpent,
    required this.redeemedAt,
  });

  factory RewardRedemption.fromJson(Map<String, dynamic> json) {
    return RewardRedemption(
      id: json['id'],
      reward: Reward.fromJson(json['reward']),
      pointsSpent: json['points_spent'],
      redeemedAt: DateTime.parse(json['redeemed_at']),
    );
  }
}

class ReferralStats {
  final int totalReferrals;
  final int activeReferrals;
  final int totalPointsEarned;
  final int currentPoints;
  final int pointsFromReferrals;
  final Map<String, int> referralsByStatus;
  final List<PointsTransaction> recentActivity;

  ReferralStats({
    required this.totalReferrals,
    required this.activeReferrals,
    required this.totalPointsEarned,
    required this.currentPoints,
    required this.pointsFromReferrals,
    required this.referralsByStatus,
    required this.recentActivity,
  });

  factory ReferralStats.fromJson(Map<String, dynamic> json) {
    return ReferralStats(
      totalReferrals: json['total_referrals'],
      activeReferrals: json['active_referrals'],
      totalPointsEarned: json['total_points_earned'],
      currentPoints: json['current_points'],
      pointsFromReferrals: json['points_from_referrals'],
      referralsByStatus: Map<String, int>.from(json['referrals_by_status']),
      recentActivity: (json['recent_activity'] as List)
          .map((item) => PointsTransaction.fromJson(item))
          .toList(),
    );
  }
}

class LeaderboardEntry {
  final int rank;
  final String userName;
  final String userId;
  final int totalReferrals;
  final int totalPoints;
  final bool isCurrentUser;

  LeaderboardEntry({
    required this.rank,
    required this.userName,
    required this.userId,
    required this.totalReferrals,
    required this.totalPoints,
    required this.isCurrentUser,
  });

  factory LeaderboardEntry.fromJson(Map<String, dynamic> json) {
    return LeaderboardEntry(
      rank: json['rank'],
      userName: json['user_name'],
      userId: json['user_id'],
      totalReferrals: json['total_referrals'],
      totalPoints: json['total_points'],
      isCurrentUser: json['is_current_user'],
    );
  }

  String get rankEmoji {
    switch (rank) {
      case 1:
        return '🥇';
      case 2:
        return '🥈';
      case 3:
        return '🥉';
      default:
        return '🏅';
    }
  }
}
