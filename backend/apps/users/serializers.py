"""
Serializers for User Model
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, MotivationalMessage, JobAlertPreference


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    profile_completion = serializers.ReadOnlyField(source='profile_completion_percentage')
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'name', 'username', 'phone', 'location', 'age',
            'experience', 'education', 'skills', 'profile_image', 'resume',
            'is_active', 'email_verified', 'points', 'created_at', 'updated_at',
            'profile_completion'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'email_verified', 'points']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = User
        fields = ['email', 'name', 'password']
    
    def create(self, validated_data):
        # Generar username automáticamente desde el email
        username = validated_data['email'].split('@')[0]
        
        # Si el username ya existe, agregar un número
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        user = User.objects.create_user(
            username=username,
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile"""
    
    class Meta:
        model = User
        fields = [
            'name', 'phone', 'location', 'experience', 'education',
            'skills', 'profile_image', 'resume'
        ]
    
    def validate_skills(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Skills debe ser una lista de strings.")
        return value


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change"""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "Las contraseñas no coinciden."})
        return attrs


class FCMTokenSerializer(serializers.Serializer):
    """Serializer for FCM token registration"""
    fcm_token = serializers.CharField(required=True, max_length=255)


class MotivationalMessageSerializer(serializers.ModelSerializer):
    """Serializer for motivational messages"""
    
    class Meta:
        model = MotivationalMessage
        fields = ['id', 'message', 'author', 'category', 'created_at']
        read_only_fields = ['id', 'created_at']


class JobAlertPreferenceSerializer(serializers.ModelSerializer):
    """Serializer for job alert preferences"""
    
    class Meta:
        model = JobAlertPreference
        fields = [
            'id', 'is_enabled', 'frequency', 'match_by_skills', 
            'match_by_location', 'match_by_experience', 'preferred_job_types',
            'preferred_locations', 'remote_only', 'min_salary', 'last_alert_sent',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'last_alert_sent', 'created_at', 'updated_at']
