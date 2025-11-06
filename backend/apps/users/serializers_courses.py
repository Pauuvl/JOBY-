from rest_framework import serializers
from .models_courses import Company, Course, UserCourse


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'logo_url', 'website', 'description', 'is_active']


class CourseSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    duration_display = serializers.ReadOnlyField()
    match_score = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'company', 'required_skills', 'skills_taught',
            'level', 'duration_value', 'duration_unit', 'duration_display',
            'course_url', 'thumbnail_url', 'is_free', 'price', 'currency',
            'rating', 'enrollments', 'match_score', 'created_at'
        ]
    
    def get_match_score(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user_skills = request.user.skills if request.user.skills else []
            return obj.calculate_match_score(user_skills)
        return 0


class UserCourseSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    
    class Meta:
        model = UserCourse
        fields = [
            'id', 'course', 'status', 'progress_percentage',
            'enrolled_at', 'completed_at', 'last_accessed'
        ]


class CourseEnrollSerializer(serializers.Serializer):
    course_id = serializers.UUIDField()
    
    def validate_course_id(self, value):
        if not Course.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError("El curso no existe o no está activo")
        return value
