"""
Views for referral and points system
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Sum, Q
from django.db import transaction
from django.contrib.auth import get_user_model

from .models_referral import (
    ReferralCode, Referral, PointsTransaction, 
    Reward, RewardRedemption
)
from .serializers_referral import (
    ReferralCodeSerializer, ReferralSerializer,
    PointsTransactionSerializer, RewardSerializer,
    RewardRedemptionSerializer, ReferralStatsSerializer
)

User = get_user_model()


class ReferralViewSet(viewsets.GenericViewSet):
    """ViewSet for referral system"""
    
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def my_code(self, request):
        """
        Get or create user's referral code
        GET /api/auth/referral/my_code/
        """
        # Get or create referral code
        referral_code, created = ReferralCode.objects.get_or_create(
            user=request.user
        )
        
        serializer = ReferralCodeSerializer(referral_code)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_referrals(self, request):
        """
        Get list of user's referrals
        GET /api/auth/referral/my_referrals/
        """
        referrals = Referral.objects.filter(
            referrer=request.user
        ).select_related('referred').order_by('-referred_at')
        
        serializer = ReferralSerializer(referrals, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Get referral statistics
        GET /api/auth/referral/stats/
        """
        user = request.user
        
        # Get referral code
        try:
            referral_code = user.referral_code
        except ReferralCode.DoesNotExist:
            referral_code = ReferralCode.objects.create(user=user)
        
        # Get all referrals
        referrals = Referral.objects.filter(referrer=user)
        
        # Count by status
        status_counts = referrals.values('status').annotate(
            count=Count('id')
        )
        referrals_by_status = {
            item['status']: item['count'] 
            for item in status_counts
        }
        
        # Points from referrals
        points_from_referrals = PointsTransaction.objects.filter(
            user=user,
            transaction_type__startswith='referral_'
        ).aggregate(total=Sum('points'))['total'] or 0
        
        # Recent activity (last 10 transactions)
        recent_transactions = PointsTransaction.objects.filter(
            user=user
        )[:10]
        recent_activity = PointsTransactionSerializer(
            recent_transactions, 
            many=True
        ).data
        
        stats = {
            'total_referrals': referral_code.total_referrals,
            'active_referrals': referrals.filter(
                status__in=['registered', 'profile_completed', 'employed']
            ).count(),
            'total_points_earned': referral_code.total_points_earned,
            'current_points': user.points,
            'points_from_referrals': points_from_referrals,
            'referrals_by_status': referrals_by_status,
            'recent_activity': recent_activity
        }
        
        serializer = ReferralStatsSerializer(stats)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def leaderboard(self, request):
        """
        Get top referrers leaderboard
        GET /api/auth/referral/leaderboard/?limit=10
        """
        limit = int(request.query_params.get('limit', 10))
        
        # Get top referrers
        top_referrers = ReferralCode.objects.filter(
            is_active=True,
            total_referrals__gt=0
        ).select_related('user').order_by(
            '-total_referrals',
            '-total_points_earned'
        )[:limit]
        
        leaderboard = []
        for idx, ref_code in enumerate(top_referrers, 1):
            leaderboard.append({
                'rank': idx,
                'user_name': ref_code.user.name,
                'user_id': str(ref_code.user.id),
                'total_referrals': ref_code.total_referrals,
                'total_points': ref_code.total_points_earned,
                'is_current_user': ref_code.user.id == request.user.id
            })
        
        return Response(leaderboard)


class PointsViewSet(viewsets.GenericViewSet):
    """ViewSet for points system"""
    
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def balance(self, request):
        """
        Get user's current points balance
        GET /api/auth/points/balance/
        """
        return Response({
            'points': request.user.points,
            'user_id': str(request.user.id),
            'user_name': request.user.name
        })
    
    @action(detail=False, methods=['get'])
    def history(self, request):
        """
        Get points transaction history
        GET /api/auth/points/history/?limit=50
        """
        limit = int(request.query_params.get('limit', 50))
        
        transactions = PointsTransaction.objects.filter(
            user=request.user
        ).select_related('related_user')[:limit]
        
        serializer = PointsTransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def rewards(self, request):
        """
        Get available rewards
        GET /api/auth/points/rewards/
        """
        rewards = Reward.objects.filter(is_active=True)
        
        serializer = RewardSerializer(
            rewards,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def redeem(self, request):
        """
        Redeem a reward with points
        POST /api/auth/points/redeem/
        Body: {"reward_id": 1}
        """
        reward_id = request.data.get('reward_id')
        
        if not reward_id:
            return Response(
                {'error': 'reward_id es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            reward = Reward.objects.get(id=reward_id, is_active=True)
        except Reward.DoesNotExist:
            return Response(
                {'error': 'Recompensa no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        user = request.user
        
        # Validations
        if user.points < reward.points_required:
            return Response(
                {'error': 'Puntos insuficientes'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check redemption limit
        times_redeemed = RewardRedemption.objects.filter(
            user=user,
            reward=reward
        ).count()
        
        if times_redeemed >= reward.max_redemptions_per_user:
            return Response(
                {'error': 'Ya alcanzaste el límite de canjes para esta recompensa'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check total available
        if reward.total_available is not None:
            total_redeemed = reward.redemptions.count()
            if total_redeemed >= reward.total_available:
                return Response(
                    {'error': 'Esta recompensa ya no está disponible'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Perform redemption
        with transaction.atomic():
            # Deduct points
            user.points -= reward.points_required
            user.save()
            
            # Create redemption
            redemption = RewardRedemption.objects.create(
                user=user,
                reward=reward,
                points_spent=reward.points_required
            )
            
            # Create transaction record
            PointsTransaction.objects.create(
                user=user,
                transaction_type='redeem',
                points=-reward.points_required,
                description=f"Canjeado: {reward.name}"
            )
        
        serializer = RewardRedemptionSerializer(redemption)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def my_redemptions(self, request):
        """
        Get user's reward redemptions
        GET /api/auth/points/my_redemptions/
        """
        redemptions = RewardRedemption.objects.filter(
            user=request.user
        ).select_related('reward').order_by('-redeemed_at')
        
        serializer = RewardRedemptionSerializer(redemptions, many=True)
        return Response(serializer.data)


def award_points(user, transaction_type, points, description, related_user=None, related_referral=None):
    """
    Helper function to award points to a user
    """
    with transaction.atomic():
        # Update user points
        user.points += points
        user.save()
        
        # Create transaction record
        PointsTransaction.objects.create(
            user=user,
            transaction_type=transaction_type,
            points=points,
            description=description,
            related_user=related_user,
            related_referral=related_referral
        )
    
    return user.points
