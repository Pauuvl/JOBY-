from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models_courses import Company, Course, UserCourse
from .serializers_courses import CompanySerializer, CourseSerializer, UserCourseSerializer, CourseEnrollSerializer


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing courses"""
    
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Course.objects.filter(is_active=True)
    
    @action(detail=False, methods=['get'])
    def recommended(self, request):
        """Get recommended courses based on user skills"""
        user_skills = request.user.skills if request.user.skills else []
        
        if not user_skills:
            # If user has no skills, return popular courses
            courses = Course.objects.filter(is_active=True).order_by('-rating', '-enrollments')[:20]
        else:
            # Find courses that teach skills user doesn't have
            all_courses = Course.objects.filter(is_active=True)
            
            # Calculate match score for each course
            courses_with_scores = []
            for course in all_courses:
                score = course.calculate_match_score(user_skills)
                if score >= 40:  # Minimum threshold
                    courses_with_scores.append((course, score))
            
            # Sort by score
            courses_with_scores.sort(key=lambda x: x[1], reverse=True)
            courses = [c[0] for c in courses_with_scores[:20]]
        
        serializer = self.get_serializer(courses, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_company(self, request):
        """Get courses by company"""
        company_id = request.query_params.get('company_id')
        
        if not company_id:
            return Response(
                {'error': 'company_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        courses = Course.objects.filter(company_id=company_id, is_active=True)
        serializer = self.get_serializer(courses, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search courses by title or skills"""
        query = request.query_params.get('q', '')
        
        if not query:
            return Response({'courses': []})
        
        courses = Course.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(skills_taught__contains=[query]),
            is_active=True
        )
        
        serializer = self.get_serializer(courses, many=True, context={'request': request})
        return Response(serializer.data)


class UserCourseViewSet(viewsets.ModelViewSet):
    """ViewSet for managing user course enrollments"""
    
    serializer_class = UserCourseSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserCourse.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def enroll(self, request):
        """Enroll user in a course"""
        serializer = CourseEnrollSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        course_id = serializer.validated_data['course_id']
        course = Course.objects.get(id=course_id)
        
        # Check if already enrolled
        existing = UserCourse.objects.filter(user=request.user, course=course).first()
        if existing:
            return Response(
                {'message': 'Ya estás inscrito en este curso', 'enrollment': UserCourseSerializer(existing).data},
                status=status.HTTP_200_OK
            )
        
        # Create enrollment
        enrollment = UserCourse.objects.create(
            user=request.user,
            course=course
        )
        
        # Award points for enrolling
        from apps.streaks.services import StreakService
        StreakService.award_points(
            request.user,
            'course_enrolled',
            10,
            f'Inscrito en: {course.title}'
        )
        
        return Response(
            UserCourseSerializer(enrollment).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'])
    def update_progress(self, request, pk=None):
        """Update course progress"""
        enrollment = self.get_object()
        progress = request.data.get('progress_percentage', 0)
        
        if not isinstance(progress, int) or progress < 0 or progress > 100:
            return Response(
                {'error': 'progress_percentage debe ser un número entre 0 y 100'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        enrollment.progress_percentage = progress
        
        # Check if completed
        if progress == 100 and enrollment.status != 'completed':
            from django.utils import timezone
            enrollment.status = 'completed'
            enrollment.completed_at = timezone.now()
            
            # Award points for completing
            from apps.streaks.services import StreakService
            StreakService.award_points(
                request.user,
                'course_completed',
                50,
                f'Curso completado: {enrollment.course.title}'
            )
        elif progress > 0:
            enrollment.status = 'in_progress'
        
        enrollment.save()
        
        return Response(UserCourseSerializer(enrollment).data)
    
    @action(detail=False, methods=['get'])
    def in_progress(self, request):
        """Get courses in progress"""
        enrollments = UserCourse.objects.filter(
            user=request.user,
            status='in_progress'
        )
        serializer = self.get_serializer(enrollments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def completed(self, request):
        """Get completed courses"""
        enrollments = UserCourse.objects.filter(
            user=request.user,
            status='completed'
        )
        serializer = self.get_serializer(enrollments, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_companies(request):
    """Get all active companies"""
    companies = Company.objects.filter(is_active=True)
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data)
