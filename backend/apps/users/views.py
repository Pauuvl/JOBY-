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

from .models import User
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileUpdateSerializer,
    ChangePasswordSerializer,
    FCMTokenSerializer,
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
