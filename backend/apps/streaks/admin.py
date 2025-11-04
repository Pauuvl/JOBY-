from django.contrib import admin
from .models import Streak, Achievement, UserAchievement, PointsHistory, Leaderboard


@admin.register(Streak)
class StreakAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_streak', 'longest_streak', 'last_activity_date', 'total_applications']
    list_filter = ['last_activity_date']
    search_fields = ['user__email', 'user__name']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'achievement_type', 'points_reward', 'requirement_type', 'requirement_value', 'is_active']
    list_filter = ['achievement_type', 'is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at']


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement', 'earned_at']
    list_filter = ['earned_at', 'achievement__achievement_type']
    search_fields = ['user__email', 'user__name', 'achievement__name']
    readonly_fields = ['id', 'earned_at']


@admin.register(PointsHistory)
class PointsHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'points', 'description', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['user__email', 'user__name', 'description']
    readonly_fields = ['id', 'created_at']


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['user', 'period', 'rank', 'points', 'period_start', 'period_end']
    list_filter = ['period', 'period_start']
    search_fields = ['user__email', 'user__name']
    readonly_fields = ['id', 'updated_at']
