from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StreakViewSet, AchievementViewSet, PointsHistoryViewSet,
    LeaderboardViewSet, StatsViewSet, ChallengeViewSet, UserChallengeViewSet
)

router = DefaultRouter()
router.register(r'streaks', StreakViewSet, basename='streak')
router.register(r'achievements', AchievementViewSet, basename='achievement')
router.register(r'points-history', PointsHistoryViewSet, basename='points-history')
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')
router.register(r'stats', StatsViewSet, basename='stats')
router.register(r'challenges', ChallengeViewSet, basename='challenge')
router.register(r'user-challenges', UserChallengeViewSet, basename='user-challenge')

urlpatterns = [
    path('', include(router.urls)),
]
