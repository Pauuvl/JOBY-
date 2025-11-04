from rest_framework import serializers
from .models import Streak, Achievement, UserAchievement, PointsHistory, Leaderboard, Challenge, UserChallenge


class StreakSerializer(serializers.ModelSerializer):
    """Serializer for Streak model"""
    
    user_name = serializers.CharField(source='user.name', read_only=True)
    
    class Meta:
        model = Streak
        fields = [
            'id', 'user', 'user_name', 'current_streak', 'longest_streak',
            'last_activity_date', 'total_logins', 'total_applications',
            'total_profile_updates', 'total_jobs_saved', 'total_jobs_viewed',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class AchievementSerializer(serializers.ModelSerializer):
    """Serializer for Achievement model"""
    
    is_earned = serializers.SerializerMethodField()
    
    class Meta:
        model = Achievement
        fields = [
            'id', 'name', 'description', 'achievement_type', 'icon',
            'points_reward', 'requirement_type', 'requirement_value',
            'is_earned'
        ]
    
    def get_is_earned(self, obj):
        """Check if current user has earned this achievement"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserAchievement.objects.filter(
                user=request.user,
                achievement=obj
            ).exists()
        return False


class UserAchievementSerializer(serializers.ModelSerializer):
    """Serializer for UserAchievement model"""
    
    achievement_details = AchievementSerializer(source='achievement', read_only=True)
    
    class Meta:
        model = UserAchievement
        fields = ['id', 'user', 'achievement', 'achievement_details', 'earned_at']
        read_only_fields = ['id', 'user', 'earned_at']


class PointsHistorySerializer(serializers.ModelSerializer):
    """Serializer for PointsHistory model"""
    
    class Meta:
        model = PointsHistory
        fields = ['id', 'user', 'action', 'points', 'description', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for Leaderboard model"""
    
    user_name = serializers.CharField(source='user.name', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Leaderboard
        fields = [
            'id', 'user', 'user_name', 'user_email', 'period', 'rank',
            'points', 'period_start', 'period_end', 'updated_at'
        ]


class UserStatsSerializer(serializers.Serializer):
    """Serializer for comprehensive user statistics"""
    
    streak = serializers.DictField()
    activity = serializers.DictField()
    points = serializers.DictField()
    achievements = serializers.DictField()


class ChallengeSerializer(serializers.ModelSerializer):
    """Serializer for Challenge model"""
    
    is_available = serializers.SerializerMethodField()
    user_progress = serializers.SerializerMethodField()
    
    class Meta:
        model = Challenge
        fields = [
            'id', 'title', 'description', 'icon', 'challenge_type', 'category',
            'target_action', 'target_count', 'points_reward', 'bonus_multiplier',
            'is_active', 'start_date', 'end_date', 'priority', 'is_available',
            'user_progress', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_is_available(self, obj):
        """Check if challenge is currently available"""
        return obj.is_available()
    
    def get_user_progress(self, obj):
        """Get current user's progress on this challenge if exists"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                user_challenge = UserChallenge.objects.filter(
                    user=request.user,
                    challenge=obj,
                    status='active'
                ).order_by('-started_at').first()
                
                if user_challenge:
                    return {
                        'id': str(user_challenge.id),
                        'current_progress': user_challenge.current_progress,
                        'progress_percentage': user_challenge.progress_percentage,
                        'status': user_challenge.status,
                        'started_at': user_challenge.started_at,
                    }
            except UserChallenge.DoesNotExist:
                pass
        return None


class UserChallengeSerializer(serializers.ModelSerializer):
    """Serializer for UserChallenge model"""
    
    challenge_details = ChallengeSerializer(source='challenge', read_only=True)
    progress_percentage = serializers.ReadOnlyField()
    is_completed = serializers.ReadOnlyField()
    
    class Meta:
        model = UserChallenge
        fields = [
            'id', 'user', 'challenge', 'challenge_details', 
            'current_progress', 'status', 'progress_percentage', 'is_completed',
            'started_at', 'completed_at', 'expires_at', 'points_earned'
        ]
        read_only_fields = ['id', 'user', 'started_at', 'completed_at', 'points_earned']


class ChallengeProgressSerializer(serializers.Serializer):
    """Serializer for updating challenge progress"""
    
    challenge_id = serializers.UUIDField(required=True)
    increment = serializers.IntegerField(default=1, min_value=1)
