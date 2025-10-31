"""
Serializers for User Model
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    profile_completion = serializers.ReadOnlyField(source='profile_completion_percentage')
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'name', 'username', 'phone', 'location',
            'experience', 'education', 'skills', 'profile_image', 'resume',
            'is_active', 'email_verified', 'created_at', 'updated_at',
            'profile_completion'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'email_verified']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['email', 'name', 'username', 'password', 'password_confirm']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
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
