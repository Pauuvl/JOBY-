from rest_framework import serializers
from .models import Job, SavedJob


class JobSerializer(serializers.ModelSerializer):
    """Serializer for Job model"""
    
    posted_by_name = serializers.CharField(source='posted_by.name', read_only=True)
    posted_by_email = serializers.EmailField(source='posted_by.email', read_only=True)
    salary_range = serializers.CharField(read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    is_saved = serializers.SerializerMethodField()
    
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'company_name', 'company_logo', 'location', 'remote_ok',
            'job_type', 'experience_level', 'description', 'requirements',
            'responsibilities', 'benefits', 'skills_required', 'salary_min',
            'salary_max', 'salary_currency', 'salary_range', 'application_url',
            'application_email', 'posted_by', 'posted_by_name', 'posted_by_email',
            'posted_at', 'updated_at', 'expires_at', 'is_active', 'views_count',
            'slug', 'is_expired', 'is_saved'
        ]
        read_only_fields = ['id', 'posted_by', 'posted_at', 'updated_at', 'views_count', 'slug']
    
    def get_is_saved(self, obj):
        """Check if current user has saved this job"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return SavedJob.objects.filter(user=request.user, job=obj).exists()
        return False


class JobCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating jobs"""
    
    class Meta:
        model = Job
        fields = [
            'title', 'company_name', 'company_logo', 'location', 'remote_ok',
            'job_type', 'experience_level', 'description', 'requirements',
            'responsibilities', 'benefits', 'skills_required', 'salary_min',
            'salary_max', 'salary_currency', 'application_url', 'application_email',
            'expires_at'
        ]
    
    def create(self, validated_data):
        # Set posted_by from request user
        request = self.context.get('request')
        validated_data['posted_by'] = request.user
        return super().create(validated_data)


class JobListSerializer(serializers.ModelSerializer):
    """Simplified serializer for job listings"""
    
    posted_by_name = serializers.CharField(source='posted_by.name', read_only=True)
    salary_range = serializers.CharField(read_only=True)
    is_saved = serializers.SerializerMethodField()
    
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'company_name', 'company_logo', 'location', 'remote_ok',
            'job_type', 'experience_level', 'salary_range', 'posted_by_name',
            'posted_at', 'slug', 'is_saved', 'views_count'
        ]
    
    def get_is_saved(self, obj):
        """Check if current user has saved this job"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return SavedJob.objects.filter(user=request.user, job=obj).exists()
        return False


class SavedJobSerializer(serializers.ModelSerializer):
    """Serializer for saved jobs"""
    
    job = JobListSerializer(read_only=True)
    job_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = SavedJob
        fields = ['id', 'user', 'job', 'job_id', 'saved_at']
        read_only_fields = ['id', 'user', 'saved_at']
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)
