"""
Views for User Authentication and Profile Management
"""
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db import transaction

from .models import User, MotivationalMessage
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileUpdateSerializer,
    ChangePasswordSerializer,
    FCMTokenSerializer,
    MotivationalMessageSerializer,
)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Register a new user
    POST /api/auth/register/
    """
    print(f"DEBUG - Register request data: {request.data}")  # Debug
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        with transaction.atomic():
            user = serializer.save()
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'Usuario registrado exitosamente',
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
    
    print(f"DEBUG - Serializer errors: {serializer.errors}")  # Debug
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Login user and return JWT tokens
    POST /api/auth/login/
    """
    print(f"DEBUG - Login request data: {request.data}")
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        # Authenticate user directly with email (USERNAME_FIELD = 'email')
        authenticated_user = authenticate(request, username=email, password=password)
        
        if authenticated_user is not None:
            if authenticated_user.is_active:
                # Generate JWT tokens
                refresh = RefreshToken.for_user(authenticated_user)
                
                return Response({
                    'message': 'Login exitoso',
                    'user': UserSerializer(authenticated_user).data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Cuenta desactivada'
                }, status=status.HTTP_403_FORBIDDEN)
        else:
            print(f"DEBUG - Login failed for {email}")
            return Response({
                'error': 'Credenciales inválidas'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    print(f"DEBUG - Serializer errors: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """
    Logout user by blacklisting refresh token
    POST /api/auth/logout/
    """
    try:
        refresh_token = request.data.get('refresh_token')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({
            'message': 'Logout exitoso'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': 'Token inválido'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """
    Get current authenticated user profile
    GET /api/auth/me/
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Update user profile
    PUT /api/auth/profile/
    """
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileUpdateView(generics.UpdateAPIView):
    """
    Update user profile
    PUT/PATCH /api/auth/profile/update/
    """
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            
            # Record profile update activity for streaks
            from apps.streaks.services import StreakService
            StreakService.record_activity(
                user=instance,
                activity_type='profile_updated',
                description='Perfil actualizado',
                points=15
            )
            
            return Response({
                'message': 'Perfil actualizado exitosamente (+15 puntos)',
                'user': UserSerializer(instance).data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    Change user password
    POST /api/auth/change-password/
    """
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        
        # Check old password
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({
                'error': 'Contraseña actual incorrecta'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Set new password
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({
            'message': 'Contraseña cambiada exitosamente'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_fcm_token(request):
    """
    Register FCM token for push notifications
    POST /api/auth/register-fcm-token/
    """
    serializer = FCMTokenSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        user.fcm_token = serializer.validated_data['fcm_token']
        user.save()
        
        return Response({
            'message': 'Token FCM registrado exitosamente'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_motivational_message(request):
    """
    Get a random motivational message for the home screen
    GET /api/motivational-message/
    
    Query params:
    - category: Filter by category (optional)
    """
    import random
    
    category = request.query_params.get('category', None)
    
    # Get active messages
    messages = MotivationalMessage.objects.filter(is_active=True)
    
    if category:
        messages = messages.filter(category=category)
    
    if not messages.exists():
        return Response({
            'message': '¡Cada día es una nueva oportunidad para crecer! 🌟',
            'author': 'Joby Team',
            'category': 'motivation'
        }, status=status.HTTP_200_OK)
    
    # Weight by priority (higher priority = more likely to be selected)
    messages_list = list(messages)
    weights = [msg.priority + 1 for msg in messages_list]  # +1 to avoid zero weight
    
    selected_message = random.choices(messages_list, weights=weights, k=1)[0]
    
    # Increment shown count
    selected_message.increment_shown_count()
    
    serializer = MotivationalMessageSerializer(selected_message)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_daily_message(request):
    """
    Get daily motivational message (same message for the entire day)
    GET /api/daily-message/
    
    Returns the same message for all users throughout the day
    """
    from django.utils import timezone
    from django.core.cache import cache
    import random
    
    # Create a cache key based on today's date
    today = timezone.now().date()
    cache_key = f'daily_message_{today}'
    
    # Try to get from cache
    cached_message = cache.get(cache_key)
    
    if cached_message:
        return Response(cached_message, status=status.HTTP_200_OK)
    
    # Get active messages
    messages = MotivationalMessage.objects.filter(is_active=True)
    
    if not messages.exists():
        message_data = {
            'message': '¡Cada día es una nueva oportunidad para crecer! 🌟',
            'author': 'Joby Team',
            'category': 'motivation'
        }
    else:
        # Select message based on day of year (deterministic for the day)
        day_of_year = today.timetuple().tm_yday
        messages_list = list(messages)
        selected_message = messages_list[day_of_year % len(messages_list)]
        
        # Increment shown count
        selected_message.increment_shown_count()
        
        message_data = MotivationalMessageSerializer(selected_message).data
    
    # Cache for 24 hours (86400 seconds)
    cache.set(cache_key, message_data, 86400)
    
    return Response(message_data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def job_alert_preferences(request):
    """
    Get or update job alert preferences
    GET/PUT/PATCH /api/auth/job-alerts/
    """
    from .models import JobAlertPreference
    from .serializers import JobAlertPreferenceSerializer
    
    # Get or create preferences
    preferences, created = JobAlertPreference.objects.get_or_create(user=request.user)
    
    if request.method == 'GET':
        serializer = JobAlertPreferenceSerializer(preferences)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = JobAlertPreferenceSerializer(preferences, data=request.data, partial=partial)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def find_matching_jobs(request):
    """
    Find jobs that match user's profile
    GET /api/auth/matching-jobs/
    """
    from apps.jobs.services import JobMatchingService
    from apps.jobs.serializers import JobSerializer
    
    min_score = int(request.query_params.get('min_score', 60))
    limit = int(request.query_params.get('limit', 10))
    
    matching_jobs = JobMatchingService.find_matching_jobs(
        user=request.user,
        min_score=min_score,
        limit=limit
    )
    
    results = []
    for job_data in matching_jobs:
        job_info = JobSerializer(job_data['job']).data
        job_info['match_score'] = job_data['score']
        job_info['matching_skills'] = job_data['matching_skills']
        results.append(job_info)
    
    return Response({
        'count': len(results),
        'matches': results
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_job_alerts(request):
    """
    Manually check for new job alerts
    POST /api/auth/check-alerts/
    """
    from apps.jobs.services import JobMatchingService
    
    notification = JobMatchingService.check_new_jobs_for_user(request.user)
    
    if notification:
        from apps.notifications.serializers import NotificationSerializer
        return Response({
            'message': 'Alert sent successfully',
            'notification': NotificationSerializer(notification).data
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'message': 'No new matching jobs found or alerts are disabled'
        }, status=status.HTTP_200_OK)
