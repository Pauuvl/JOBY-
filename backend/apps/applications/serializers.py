from rest_framework import serializers
from .models import Application
from apps.jobs.serializers import JobListSerializer


class ApplicationSerializer(serializers.ModelSerializer):
    """Serializer for Application model"""
    
    job_details = JobListSerializer(source='job', read_only=True)
    applicant_name = serializers.CharField(source='applicant.name', read_only=True)
    applicant_email = serializers.EmailField(source='applicant.email', read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Application
        fields = [
            'id', 'job', 'job_details', 'applicant', 'applicant_name', 'applicant_email',
            'cover_letter', 'resume', 'portfolio_url', 'status', 'status_notes',
            'applied_at', 'updated_at', 'reviewed_at', 'interview_scheduled_at',
            'interview_location', 'interview_notes', 'is_active'
        ]
        read_only_fields = ['id', 'applicant', 'applied_at', 'updated_at']


class ApplicationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating applications"""
    
    class Meta:
        model = Application
        fields = ['job', 'cover_letter', 'resume', 'portfolio_url']
    
    def validate(self, data):
        """Check if user already applied to this job"""
        request = self.context.get('request')
        job = data.get('job')
        
        if Application.objects.filter(job=job, applicant=request.user).exists():
            raise serializers.ValidationError("You have already applied to this job.")
        
        return data
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['applicant'] = request.user
        return super().create(validated_data)


class ApplicationListSerializer(serializers.ModelSerializer):
    """Simplified serializer for application listings"""
    
    job_title = serializers.CharField(source='job.title', read_only=True)
    company_name = serializers.CharField(source='job.company_name', read_only=True)
    applicant_name = serializers.CharField(source='applicant.name', read_only=True)
    
    class Meta:
        model = Application
        fields = [
            'id', 'job', 'job_title', 'company_name', 'applicant_name',
            'status', 'applied_at', 'interview_scheduled_at'
        ]


class ApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating application status"""
    
    class Meta:
        model = Application
        fields = ['status', 'status_notes', 'reviewed_at', 'interview_scheduled_at', 
                  'interview_location', 'interview_notes']
