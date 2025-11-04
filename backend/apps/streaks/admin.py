from django.contrib import admin
from .models import Streak, Achievement, UserAchievement, PointsHistory, Leaderboard, Challenge, UserChallenge


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


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['title', 'challenge_type', 'category', 'target_count', 'points_reward', 'is_active', 'start_date', 'end_date']
    list_filter = ['challenge_type', 'category', 'is_active', 'start_date']
    search_fields = ['title', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('title', 'description', 'icon', 'challenge_type', 'category')
        }),
        ('Configuración del reto', {
            'fields': ('target_count', 'points_reward', 'is_active')
        }),
        ('Disponibilidad', {
            'fields': ('start_date', 'end_date'),
            'description': 'Deja en blanco para que el reto esté siempre disponible'
        }),
        ('Metadatos', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserChallenge)
class UserChallengeAdmin(admin.ModelAdmin):
    list_display = ['user', 'challenge', 'status', 'current_progress', 'target_count', 'progress_percentage_display', 'started_at', 'completed_at']
    list_filter = ['status', 'started_at', 'completed_at', 'challenge__challenge_type']
    search_fields = ['user__email', 'user__name', 'challenge__title']
    readonly_fields = ['id', 'started_at', 'completed_at', 'progress_percentage', 'is_completed']
    
    def progress_percentage_display(self, obj):
        return f"{obj.progress_percentage:.1f}%"
    progress_percentage_display.short_description = 'Progreso'
    
    def target_count(self, obj):
        return obj.challenge.target_count
    target_count.short_description = 'Meta'
    
    fieldsets = (
        ('Información del usuario y reto', {
            'fields': ('user', 'challenge')
        }),
        ('Progreso', {
            'fields': ('current_progress', 'status', 'progress_percentage', 'is_completed')
        }),
        ('Puntos', {
            'fields': ('points_earned',)
        }),
        ('Fechas', {
            'fields': ('started_at', 'completed_at', 'expires_at')
        }),
        ('Metadatos', {
            'fields': ('id',),
            'classes': ('collapse',)
        }),
    )
