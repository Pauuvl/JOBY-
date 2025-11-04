from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from .models import Application
from .serializers import (
    ApplicationSerializer, ApplicationCreateSerializer,
    ApplicationListSerializer, ApplicationStatusUpdateSerializer
)


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Application CRUD operations
    
    list: Get all applications (filtered by user role)
    retrieve: Get a specific application
    create: Apply to a job
    update/partial_update: Update application status
    destroy: Withdraw application
    """
    
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return applications based on user:
        - Regular users see their own applications
        - Job posters see applications to their jobs
        """
        user = self.request.user
        
        # If filtering by job (for job posters)
        job_id = self.request.query_params.get('job_id')
        if job_id:
            # Return applications to jobs posted by this user
            return Application.objects.filter(job__posted_by=user, job__id=job_id)
        
        # Default: return user's own applications
        return Application.objects.filter(applicant=user)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ApplicationListSerializer
        elif self.action == 'create':
            return ApplicationCreateSerializer
        elif self.action == 'update_status':
            return ApplicationStatusUpdateSerializer
        return ApplicationSerializer
    
    def create(self, request, *args, **kwargs):
        """Apply to a job"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Award points for applying (gamification)
        request.user.points += 10
        request.user.save(update_fields=['points'])
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'message': 'Application submitted successfully!',
                'application': serializer.data,
                'points_earned': 10
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    def destroy(self, request, *args, **kwargs):
        """Withdraw application"""
        instance = self.get_object()
        
        # Only applicant can withdraw
        if instance.applicant != request.user:
            return Response(
                {'error': 'You can only withdraw your own applications'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Can't withdraw if already accepted/rejected
        if instance.status in ['accepted', 'rejected']:
            return Response(
                {'error': f'Cannot withdraw an application that is {instance.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        instance.status = 'withdrawn'
        instance.save(update_fields=['status'])
        
        return Response(
            {'message': 'Application withdrawn successfully'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def my_applications(self, request):
        """Get all applications by current user"""
        queryset = Application.objects.filter(applicant=request.user)
        
        # Filter by status if provided
        status_filter = request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        serializer = ApplicationListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def received(self, request):
        """Get applications received for jobs posted by current user"""
        queryset = Application.objects.filter(job__posted_by=request.user)
        
        # Filter by status if provided
        status_filter = request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by job if provided
        job_id = request.query_params.get('job_id')
        if job_id:
            queryset = queryset.filter(job__id=job_id)
        
        serializer = ApplicationSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Update application status (job poster only)"""
        application = self.get_object()
        
        # Only job poster can update status
        if application.job.posted_by != request.user:
            return Response(
                {'error': 'Only the job poster can update application status'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = ApplicationStatusUpdateSerializer(
            application,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        
        # Set reviewed_at if status is being changed from pending
        if application.status == 'pending' and request.data.get('status') != 'pending':
            serializer.validated_data['reviewed_at'] = timezone.now()
        
        serializer.save()
        
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get application statistics for current user"""
        user = request.user
        
        # Statistics for applicant
        applicant_stats = {
            'total': Application.objects.filter(applicant=user).count(),
            'pending': Application.objects.filter(applicant=user, status='pending').count(),
            'reviewed': Application.objects.filter(applicant=user, status='reviewed').count(),
            'interview': Application.objects.filter(applicant=user, status='interview').count(),
            'offered': Application.objects.filter(applicant=user, status='offered').count(),
            'accepted': Application.objects.filter(applicant=user, status='accepted').count(),
            'rejected': Application.objects.filter(applicant=user, status='rejected').count(),
        }
        
        # Statistics for job poster
        poster_stats = {
            'total': Application.objects.filter(job__posted_by=user).count(),
            'pending': Application.objects.filter(job__posted_by=user, status='pending').count(),
            'reviewed': Application.objects.filter(job__posted_by=user, status='reviewed').count(),
            'interview': Application.objects.filter(job__posted_by=user, status='interview').count(),
        }
        
        return Response({
            'as_applicant': applicant_stats,
            'as_poster': poster_stats
        })
