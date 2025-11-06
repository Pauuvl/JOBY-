"""
Serializers for referral and points system
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models_referral import ReferralCode, Referral, PointsTransaction, Reward, RewardRedemption

User = get_user_model()


class ReferredUserSerializer(serializers.ModelSerializer):
    """Simplified user info for referrals"""
    
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'created_at']


class ReferralSerializer(serializers.ModelSerializer):
    """Serializer for referrals"""
    
    referred = ReferredUserSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Referral
        fields = [
            'id', 'referred', 'status', 'status_display',
            'registration_points_awarded', 'profile_completion_points_awarded',
            'employment_points_awarded', 'referred_at', 'last_milestone_at'
        ]


class ReferralCodeSerializer(serializers.ModelSerializer):
    """Serializer for referral codes"""
    
    share_link = serializers.SerializerMethodField()
    share_message = serializers.SerializerMethodField()
    
    class Meta:
        model = ReferralCode
        fields = [
            'id', 'code', 'total_referrals', 'total_points_earned',
            'is_active', 'created_at', 'share_link', 'share_message'
        ]
    
    def get_share_link(self, obj):
        """Generate shareable link"""
        # TODO: Replace with actual production URL
        base_url = "https://joby.app"
        return f"{base_url}/register?ref={obj.code}"
    
    def get_share_message(self, obj):
        """Generate share message"""
        link = self.get_share_link(obj)
        return (
            f"🚀 ¡Únete a JOBY y encuentra tu trabajo ideal!\n\n"
            f"Usa mi código {obj.code} y recibe 20 puntos de bienvenida.\n\n"
            f"Descarga la app: {link}\n\n"
            f"#JOBY #EmpleoFácil #TrabajoRemoto"
        )


class PointsTransactionSerializer(serializers.ModelSerializer):
    """Serializer for points transactions"""
    
    transaction_type_display = serializers.CharField(
        source='get_transaction_type_display',
        read_only=True
    )
    related_user_name = serializers.CharField(
        source='related_user.name',
        read_only=True,
        allow_null=True
    )
    
    class Meta:
        model = PointsTransaction
        fields = [
            'id', 'transaction_type', 'transaction_type_display',
            'points', 'description', 'related_user_name',
            'created_at'
        ]


class RewardSerializer(serializers.ModelSerializer):
    """Serializer for rewards"""
    
    reward_type_display = serializers.CharField(
        source='get_reward_type_display',
        read_only=True
    )
    can_redeem = serializers.SerializerMethodField()
    times_redeemed = serializers.SerializerMethodField()
    
    class Meta:
        model = Reward
        fields = [
            'id', 'name', 'description', 'reward_type', 'reward_type_display',
            'points_required', 'icon', 'is_active', 'max_redemptions_per_user',
            'total_available', 'can_redeem', 'times_redeemed'
        ]
    
    def get_can_redeem(self, obj):
        """Check if user can redeem this reward"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        
        user = request.user
        
        # Check points
        if user.points < obj.points_required:
            return False
        
        # Check redemption limit
        times_redeemed = RewardRedemption.objects.filter(
            user=user,
            reward=obj
        ).count()
        
        if times_redeemed >= obj.max_redemptions_per_user:
            return False
        
        # Check total available
        if obj.total_available is not None:
            total_redeemed = obj.redemptions.count()
            if total_redeemed >= obj.total_available:
                return False
        
        return True
    
    def get_times_redeemed(self, obj):
        """Get how many times user redeemed this"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return 0
        
        return RewardRedemption.objects.filter(
            user=request.user,
            reward=obj
        ).count()


class RewardRedemptionSerializer(serializers.ModelSerializer):
    """Serializer for reward redemptions"""
    
    reward = RewardSerializer(read_only=True)
    
    class Meta:
        model = RewardRedemption
        fields = ['id', 'reward', 'points_spent', 'redeemed_at']


class ReferralStatsSerializer(serializers.Serializer):
    """Statistics for referral system"""
    
    total_referrals = serializers.IntegerField()
    active_referrals = serializers.IntegerField()
    total_points_earned = serializers.IntegerField()
    current_points = serializers.IntegerField()
    points_from_referrals = serializers.IntegerField()
    referrals_by_status = serializers.DictField()
    recent_activity = serializers.ListField()


class UseReferralCodeSerializer(serializers.Serializer):
    """Serializer for using a referral code during registration"""
    
    referral_code = serializers.CharField(max_length=10, required=True)
    
    def validate_referral_code(self, value):
        """Validate that referral code exists and is active"""
        try:
            code = ReferralCode.objects.get(code=value.upper(), is_active=True)
            return code
        except ReferralCode.DoesNotExist:
            raise serializers.ValidationError("Código de referido no válido")
