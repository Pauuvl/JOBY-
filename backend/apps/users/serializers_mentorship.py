"""
Serializers for mentorship system
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models_mentorship import SuccessStory, ProfileMatch, MentorshipRequest

User = get_user_model()


class MentorUserSerializer(serializers.ModelSerializer):
    """Simplified user serializer for mentor display"""
    
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'location', 'skills', 'experience']


class SuccessStorySerializer(serializers.ModelSerializer):
    """Serializer for success stories"""
    
    user = MentorUserSerializer(read_only=True)
    status_display = serializers.SerializerMethodField()
    
    class Meta:
        model = SuccessStory
        fields = [
            'id', 'user', 'company', 'position', 'hire_date',
            'salary_range', 'is_willing_to_mentor', 'max_mentees',
            'success_description', 'key_skills_used',
            'current_mentees_count', 'can_accept_mentees',
            'status_display', 'created_at'
        ]
    
    def get_status_display(self, obj):
        if obj.can_accept_mentees:
            return "Disponible"
        elif not obj.is_willing_to_mentor:
            return "No disponible"
        else:
            return "Capacidad completa"


class ProfileMatchSerializer(serializers.ModelSerializer):
    """Serializer for profile matches"""
    
    matched_user = MentorUserSerializer(read_only=True)
    success_story = serializers.SerializerMethodField()
    
    class Meta:
        model = ProfileMatch
        fields = [
            'id', 'matched_user', 'similarity_score',
            'matching_skills', 'skill_overlap_percentage',
            'same_location', 'similar_experience_level',
            'success_story', 'calculated_at'
        ]
    
    def get_success_story(self, obj):
        """Include success story if available"""
        try:
            story = obj.matched_user.success_story
            return SuccessStorySerializer(story).data
        except SuccessStory.DoesNotExist:
            return None


class MentorshipRequestSerializer(serializers.ModelSerializer):
    """Serializer for mentorship requests"""
    
    from_user = MentorUserSerializer(read_only=True)
    to_user = MentorUserSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = MentorshipRequest
        fields = [
            'id', 'from_user', 'to_user', 'status', 'status_display',
            'message', 'response_message', 'responded_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['from_user', 'status', 'responded_at']


class SendMentorshipRequestSerializer(serializers.Serializer):
    """Serializer for sending mentorship request"""
    
    to_user_id = serializers.UUIDField()
    message = serializers.CharField(max_length=1000)
    
    def validate_to_user_id(self, value):
        """Validate that mentor exists and is available"""
        try:
            user = User.objects.get(id=value)
            if not hasattr(user, 'success_story'):
                raise serializers.ValidationError(
                    "Este usuario no tiene una historia de éxito registrada"
                )
            if not user.success_story.can_accept_mentees:
                raise serializers.ValidationError(
                    "Este mentor no está disponible actualmente"
                )
        except User.DoesNotExist:
            raise serializers.ValidationError("Usuario no encontrado")
        
        return value
    
    def validate(self, data):
        """Validate no duplicate requests"""
        request = self.context.get('request')
        if request and request.user:
            existing = MentorshipRequest.objects.filter(
                from_user=request.user,
                to_user_id=data['to_user_id'],
                status='pending'
            ).exists()
            
            if existing:
                raise serializers.ValidationError(
                    "Ya tienes una solicitud pendiente con este mentor"
                )
        
        return data


class RespondMentorshipRequestSerializer(serializers.Serializer):
    """Serializer for responding to mentorship request"""
    
    action = serializers.ChoiceField(choices=['accept', 'decline'])
    response_message = serializers.CharField(max_length=500, required=False, allow_blank=True)


__all__ = [
    'SuccessStorySerializer',
    'ProfileMatchSerializer',
    'MentorshipRequestSerializer',
    'SendMentorshipRequestSerializer',
    'RespondMentorshipRequestSerializer',
]
