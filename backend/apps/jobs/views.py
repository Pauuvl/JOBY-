from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from .models import Job, SavedJob
from .serializers import (
    JobSerializer, JobCreateSerializer, JobListSerializer, SavedJobSerializer
)


class JobViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Job CRUD operations
    
    list: Get all active jobs
    retrieve: Get a specific job (increments view count)
    create: Create a new job (authenticated users only)
    update/partial_update: Update a job (owner only)
    destroy: Delete a job (owner only)
    """
    
    queryset = Job.objects.filter(is_active=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['job_type', 'experience_level', 'remote_ok']
    search_fields = ['title', 'company_name', 'location', 'description', 'skills_required']
    ordering_fields = ['posted_at', 'views_count', 'salary_min']
    ordering = ['-posted_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return JobListSerializer
        elif self.action == 'create':
            return JobCreateSerializer
        return JobSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """Increment view count when job is retrieved"""
        instance = self.get_object()
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def get_queryset(self):
        """Filter jobs based on query parameters"""
        queryset = super().get_queryset()
        
        # Filter by skills
        skills = self.request.query_params.get('skills', None)
        if skills:
            skill_list = skills.split(',')
            for skill in skill_list:
                queryset = queryset.filter(skills_required__icontains=skill.strip())
        
        # Filter by salary range
        min_salary = self.request.query_params.get('min_salary', None)
        if min_salary:
            queryset = queryset.filter(salary_min__gte=min_salary)
        
        max_salary = self.request.query_params.get('max_salary', None)
        if max_salary:
            queryset = queryset.filter(salary_max__lte=max_salary)
        
        # Filter by company
        company = self.request.query_params.get('company', None)
        if company:
            queryset = queryset.filter(company_name__icontains=company)
        
        return queryset
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_jobs(self, request):
        """Get jobs posted by the current user"""
        queryset = Job.objects.filter(posted_by=request.user)
        serializer = JobListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def recommended(self, request):
        """Get job recommendations based on user profile"""
        user = request.user
        
        # Get user skills from profile
        user_skills = user.skills if user.skills else []
        
        if not user_skills:
            # If no skills, return recent jobs
            queryset = self.get_queryset()[:10]
        else:
            # Filter jobs that match user skills
            query = Q()
            for skill in user_skills:
                query |= Q(skills_required__icontains=skill)
            
            queryset = self.get_queryset().filter(query).distinct()[:20]
        
        serializer = JobListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def save(self, request, pk=None):
        """Save a job to user's saved jobs"""
        job = self.get_object()
        saved_job, created = SavedJob.objects.get_or_create(
            user=request.user,
            job=job
        )
        
        if created:
            return Response(
                {'message': 'Job saved successfully'},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'message': 'Job already saved'},
                status=status.HTTP_200_OK
            )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unsave(self, request, pk=None):
        """Remove a job from user's saved jobs"""
        job = self.get_object()
        deleted_count, _ = SavedJob.objects.filter(
            user=request.user,
            job=job
        ).delete()
        
        if deleted_count > 0:
            return Response(
                {'message': 'Job unsaved successfully'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'message': 'Job was not saved'},
                status=status.HTTP_404_NOT_FOUND
            )


class SavedJobViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing and managing saved jobs
    
    list: Get all jobs saved by current user
    retrieve: Get a specific saved job
    """
    
    serializer_class = SavedJobSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return SavedJob.objects.filter(user=self.request.user)
