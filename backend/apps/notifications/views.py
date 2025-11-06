from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from .models import Notification, PushNotificationToken, NotificationPreference
from .serializers import (
    NotificationSerializer, PushNotificationTokenSerializer,
    NotificationPreferenceSerializer
)


class NotificationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing notifications"""
    
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Get unread notifications"""
        unread = self.get_queryset().filter(is_read=False)
        serializer = self.get_serializer(unread, many=True)
        return Response({
            'count': unread.count(),
            'notifications': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark a notification as read"""
        notification = self.get_object()
        notification.mark_as_read()
        serializer = self.get_serializer(notification)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """Mark all notifications as read"""
        updated = self.get_queryset().filter(is_read=False).update(
            is_read=True,
            read_at=timezone.now()
        )
        return Response({
            'message': f'Marked {updated} notifications as read'
        })
    
    @action(detail=False, methods=['post', 'delete'])
    def clear_all(self, request):
        """Delete all notifications"""
        deleted_count, _ = self.get_queryset().delete()
        return Response({
            'message': f'Deleted {deleted_count} notifications'
        })
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get notification statistics"""
        queryset = self.get_queryset()
        
        total = queryset.count()
        unread = queryset.filter(is_read=False).count()
        by_type = {}
        
        for notification in queryset.values('notification_type').distinct():
            n_type = notification['notification_type']
            by_type[n_type] = queryset.filter(notification_type=n_type).count()
        
        return Response({
            'total': total,
            'unread': unread,
            'read': total - unread,
            'by_type': by_type
        })


class PushNotificationTokenViewSet(viewsets.ModelViewSet):
    """ViewSet for managing push notification tokens"""
    
    serializer_class = PushNotificationTokenSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return PushNotificationToken.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        """Register a new FCM token"""
        token = request.data.get('token')
        
        # Check if token already exists
        existing = PushNotificationToken.objects.filter(token=token).first()
        
        if existing:
            # Update existing token
            existing.user = request.user
            existing.device_type = request.data.get('device_type', existing.device_type)
            existing.device_name = request.data.get('device_name', existing.device_name)
            existing.is_active = True
            existing.save()
            serializer = self.get_serializer(existing)
            return Response(serializer.data)
        
        # Create new token
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a push token"""
        token = self.get_object()
        token.is_active = False
        token.save(update_fields=['is_active'])
        return Response({'message': 'Token deactivated'})


class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    """ViewSet for managing notification preferences"""
    
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return NotificationPreference.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        """Get or update current user's notification preferences"""
        prefs, created = NotificationPreference.objects.get_or_create(user=request.user)
        
        if request.method in ['PUT', 'PATCH']:
            serializer = self.get_serializer(prefs, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(prefs)
            return Response(serializer.data)
