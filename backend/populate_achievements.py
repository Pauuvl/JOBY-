# Script to populate initial achievements
from apps.streaks.models import Achievement

# Create achievements
achievements_data = [
    # Streak achievements
    {'name': 'Getting Started', 'description': 'Complete your first day on Joby', 'achievement_type': 'streak', 'icon': '🌱', 'points_reward': 10, 'requirement_type': 'streak_days', 'requirement_value': 1},
    {'name': 'On a Roll', 'description': 'Maintain a 7-day streak', 'achievement_type': 'streak', 'icon': '🔥', 'points_reward': 50, 'requirement_type': 'streak_days', 'requirement_value': 7},
    {'name': 'Unstoppable', 'description': 'Maintain a 30-day streak', 'achievement_type': 'streak', 'icon': '💪', 'points_reward': 200, 'requirement_type': 'streak_days', 'requirement_value': 30},
    {'name': 'Legend', 'description': 'Maintain a 100-day streak', 'achievement_type': 'streak', 'icon': '👑', 'points_reward': 1000, 'requirement_type': 'streak_days', 'requirement_value': 100},
    
    # Application achievements
    {'name': 'First Step', 'description': 'Submit your first application', 'achievement_type': 'applications', 'icon': '📝', 'points_reward': 20, 'requirement_type': 'total_applications', 'requirement_value': 1},
    {'name': 'Go Getter', 'description': 'Submit 10 applications', 'achievement_type': 'applications', 'icon': '🎯', 'points_reward': 100, 'requirement_type': 'total_applications', 'requirement_value': 10},
    {'name': 'Job Hunter', 'description': 'Submit 25 applications', 'achievement_type': 'applications', 'icon': '🏹', 'points_reward': 250, 'requirement_type': 'total_applications', 'requirement_value': 25},
    {'name': 'Application Master', 'description': 'Submit 50 applications', 'achievement_type': 'applications', 'icon': '🏆', 'points_reward': 500, 'requirement_type': 'total_applications', 'requirement_value': 50},
    
    # Profile achievements
    {'name': 'Profile Complete', 'description': 'Complete your profile 100%', 'achievement_type': 'profile', 'icon': '✅', 'points_reward': 50, 'requirement_type': 'profile_completion', 'requirement_value': 100},
    
    # Milestone achievements
    {'name': 'Points Pioneer', 'description': 'Earn 100 points', 'achievement_type': 'milestone', 'icon': '⭐', 'points_reward': 25, 'requirement_type': 'total_points', 'requirement_value': 100},
    {'name': 'Points Pro', 'description': 'Earn 500 points', 'achievement_type': 'milestone', 'icon': '🌟', 'points_reward': 100, 'requirement_type': 'total_points', 'requirement_value': 500},
    {'name': 'Points Champion', 'description': 'Earn 1000 points', 'achievement_type': 'milestone', 'icon': '💫', 'points_reward': 200, 'requirement_type': 'total_points', 'requirement_value': 1000},
]

created_count = 0
for achievement_data in achievements_data:
    achievement, created = Achievement.objects.get_or_create(
        name=achievement_data['name'],
        defaults=achievement_data
    )
    if created:
        created_count += 1
        print(f"Created: {achievement.icon} {achievement.name}")

print(f"\nTotal achievements created: {created_count}/{len(achievements_data)}")
