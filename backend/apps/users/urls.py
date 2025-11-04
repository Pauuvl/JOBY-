"""
URL configuration for users app
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Profile
    path('me/', views.get_current_user, name='current_user'),
    path('profile/', views.update_profile, name='update_profile'),
    path('profile/update/', views.UserProfileUpdateView.as_view(), name='profile_update'),
    path('change-password/', views.change_password, name='change_password'),
    
    # FCM Token for push notifications
    path('register-fcm-token/', views.register_fcm_token, name='register_fcm_token'),
    
    # Motivational Messages
    path('motivational-message/', views.get_motivational_message, name='motivational_message'),
    path('daily-message/', views.get_daily_message, name='daily_message'),
]
