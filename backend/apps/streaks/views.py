from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Sum, Count, Q
from django.utils import timezone

from .models import Streak, Achievement, UserAchievement, PointsHistory, Leaderboard, Challenge, UserChallenge
from .serializers import (
    StreakSerializer, AchievementSerializer, UserAchievementSerializer,
    PointsHistorySerializer, LeaderboardSerializer, UserStatsSerializer,
    ChallengeSerializer, UserChallengeSerializer, ChallengeProgressSerializer
)
from .services import StreakService


class StreakViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing streaks"""
    
    serializer_class = StreakSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Streak.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_streak(self, request):
        """Get current user's streak"""
        streak, created = Streak.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(streak)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def record_activity(self, request):
        """Record daily activity"""
        activity_type = request.data.get('activity_type', 'login')
        
        streak_updated = StreakService.record_activity(request.user, activity_type)
        
        # Award points for daily login
        if activity_type == 'login' and streak_updated:
            StreakService.award_points(
                request.user,
                'login',
                5,
                'Daily login bonus'
            )
        
        streak = Streak.objects.get(user=request.user)
        serializer = self.get_serializer(streak)
        
        return Response({
            'streak': serializer.data,
            'streak_updated': streak_updated,
            'message': 'Activity recorded successfully'
        })


class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing achievements"""
    
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticated]
    queryset = Achievement.objects.filter(is_active=True)
    
    @action(detail=False, methods=['get'])
    def my_achievements(self, request):
        """Get achievements earned by current user"""
        earned = UserAchievement.objects.filter(user=request.user)
        serializer = UserAchievementSerializer(earned, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get achievements not yet earned"""
        earned_ids = UserAchievement.objects.filter(
            user=request.user
        ).values_list('achievement_id', flat=True)
        
        available = Achievement.objects.filter(
            is_active=True
        ).exclude(id__in=earned_ids)
        
        serializer = self.get_serializer(available, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def check_progress(self, request):
        """Check progress towards all achievements"""
        new_achievements = StreakService.check_achievements(request.user)
        
        if new_achievements:
            return Response({
                'message': f'Congratulations! You earned {len(new_achievements)} new achievement(s)!',
                'new_achievements': AchievementSerializer(new_achievements, many=True).data
            })
        else:
            return Response({
                'message': 'No new achievements earned',
                'new_achievements': []
            })


class PointsHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing points history"""
    
    serializer_class = PointsHistorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return PointsHistory.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get points summary"""
        total_earned = PointsHistory.objects.filter(
            user=request.user,
            points__gt=0
        ).aggregate(total=Sum('points'))['total'] or 0
        
        by_action = PointsHistory.objects.filter(
            user=request.user
        ).values('action').annotate(
            total=Sum('points'),
            count=Count('id')
        ).order_by('-total')
        
        return Response({
            'total_points': request.user.points,
            'total_earned': total_earned,
            'by_action': list(by_action)
        })


class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing leaderboards"""
    
    serializer_class = LeaderboardSerializer
    permission_classes = [IsAuthenticated]
    queryset = Leaderboard.objects.all()
    
    @action(detail=False, methods=['get'])
    def top_users(self, request):
        """Get top users by points"""
        period = request.query_params.get('period', 'all_time')
        limit = int(request.query_params.get('limit', 10))
        
        if period == 'all_time':
            # Get top users by total points
            from apps.users.models import User
            top_users = User.objects.order_by('-points')[:limit]
            
            leaderboard_data = [
                {
                    'rank': idx + 1,
                    'user_name': user.name,
                    'user_email': user.email,
                    'points': user.points,
                    'current_streak': getattr(user.streak, 'current_streak', 0) if hasattr(user, 'streak') else 0
                }
                for idx, user in enumerate(top_users)
            ]
        else:
            # Get from Leaderboard cache
            today = timezone.now().date()
            entries = Leaderboard.objects.filter(
                period=period,
                period_end__gte=today
            ).order_by('rank')[:limit]
            
            leaderboard_data = LeaderboardSerializer(entries, many=True).data
        
        return Response({
            'period': period,
            'leaderboard': leaderboard_data
        })
    
    @action(detail=False, methods=['get'])
    def my_rank(self, request):
        """Get current user's ranking"""
        user = request.user
        
        # Get user's rank (all time)
        from apps.users.models import User
        higher_rank_count = User.objects.filter(points__gt=user.points).count()
        rank = higher_rank_count + 1
        
        total_users = User.objects.count()
        
        return Response({
            'rank': rank,
            'total_users': total_users,
            'points': user.points,
            'percentile': round((1 - rank / total_users) * 100, 2) if total_users > 0 else 0
        })


class StatsViewSet(viewsets.ViewSet):
    """ViewSet for comprehensive user statistics"""
    
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get comprehensive statistics for current user"""
        stats = StreakService.get_user_stats(request.user)
        serializer = UserStatsSerializer(stats)
        return Response(serializer.data)


class ChallengeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing challenges"""
    
    serializer_class = ChallengeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get available challenges"""
        queryset = Challenge.objects.filter(is_active=True)
        
        # Filter by type
        challenge_type = self.request.query_params.get('type', None)
        if challenge_type:
            queryset = queryset.filter(challenge_type=challenge_type)
        
        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get all currently available challenges"""
        today = timezone.now().date()
        challenges = Challenge.objects.filter(
            is_active=True
        ).filter(
            Q(start_date__isnull=True) | Q(start_date__lte=today)
        ).filter(
            Q(end_date__isnull=True) | Q(end_date__gte=today)
        )
        
        serializer = self.get_serializer(challenges, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def daily(self, request):
        """Get today's daily challenges"""
        challenges = Challenge.objects.filter(
            is_active=True,
            challenge_type='daily'
        )
        
        serializer = self.get_serializer(challenges, many=True, context={'request': request})
        return Response({
            'date': timezone.now().date(),
            'challenges': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def weekly(self, request):
        """Get this week's challenges"""
        challenges = Challenge.objects.filter(
            is_active=True,
            challenge_type='weekly'
        )
        
        serializer = self.get_serializer(challenges, many=True, context={'request': request})
        return Response({
            'week': timezone.now().isocalendar()[1],
            'challenges': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """Start a challenge"""
        challenge = self.get_object()
        
        if not challenge.is_available():
            return Response({
                'error': 'Este reto no está disponible actualmente'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user already has an active challenge
        existing = UserChallenge.objects.filter(
            user=request.user,
            challenge=challenge,
            status='active'
        ).first()
        
        if existing:
            return Response({
                'message': 'Ya tienes este reto activo',
                'user_challenge': UserChallengeSerializer(existing).data
            })
        
        # Create new user challenge
        expires_at = None
        if challenge.challenge_type == 'daily':
            expires_at = timezone.now().replace(hour=23, minute=59, second=59)
        elif challenge.challenge_type == 'weekly':
            from datetime import timedelta
            expires_at = timezone.now() + timedelta(days=7)
        
        user_challenge = UserChallenge.objects.create(
            user=request.user,
            challenge=challenge,
            expires_at=expires_at
        )
        
        serializer = UserChallengeSerializer(user_challenge)
        return Response({
            'message': 'Reto iniciado exitosamente',
            'user_challenge': serializer.data
        }, status=status.HTTP_201_CREATED)


class UserChallengeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing user challenges"""
    
    serializer_class = UserChallengeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserChallenge.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active challenges for current user"""
        active_challenges = UserChallenge.objects.filter(
            user=request.user,
            status='active'
        )
        
        serializer = self.get_serializer(active_challenges, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def completed(self, request):
        """Get all completed challenges for current user"""
        completed = UserChallenge.objects.filter(
            user=request.user,
            status='completed'
        )
        
        serializer = self.get_serializer(completed, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def update_progress(self, request):
        """Update progress on a challenge"""
        serializer = ChallengeProgressSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        challenge_id = serializer.validated_data['challenge_id']
        increment = serializer.validated_data['increment']
        
        try:
            user_challenge = UserChallenge.objects.get(
                user=request.user,
                challenge_id=challenge_id,
                status='active'
            )
        except UserChallenge.DoesNotExist:
            return Response({
                'error': 'No tienes este reto activo'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Update progress
        points_earned = user_challenge.update_progress(increment)
        
        response_serializer = UserChallengeSerializer(user_challenge)
        response_data = {
            'message': 'Progreso actualizado',
            'user_challenge': response_serializer.data
        }
        
        if user_challenge.status == 'completed':
            response_data['message'] = f'¡Reto completado! +{points_earned} puntos'
            response_data['points_earned'] = points_earned
        
        return Response(response_data)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get challenges summary for current user"""
        total_completed = UserChallenge.objects.filter(
            user=request.user,
            status='completed'
        ).count()
        
        total_active = UserChallenge.objects.filter(
            user=request.user,
            status='active'
        ).count()
        
        total_points_from_challenges = UserChallenge.objects.filter(
            user=request.user,
            status='completed'
        ).aggregate(total=Sum('points_earned'))['total'] or 0
        
        return Response({
            'total_completed': total_completed,
            'total_active': total_active,
            'total_points_earned': total_points_from_challenges
        })
