"""
URL configuration for users app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from .views_courses import CourseViewSet, UserCourseViewSet, get_companies
from .views_mentorship import MentorshipViewSet
from .views_referral import ReferralViewSet, PointsViewSet

app_name = 'users'

# Create router for ViewSets
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'user-courses', UserCourseViewSet, basename='user-course')
router.register(r'mentorship', MentorshipViewSet, basename='mentorship')
router.register(r'referral', ReferralViewSet, basename='referral')
router.register(r'points', PointsViewSet, basename='points')

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
    
    # Job Alerts
    path('job-alerts/', views.job_alert_preferences, name='job_alert_preferences'),
    path('matching-jobs/', views.find_matching_jobs, name='find_matching_jobs'),
    path('check-alerts/', views.check_job_alerts, name='check_job_alerts'),
    
    # Courses and Companies
    path('companies/', get_companies, name='companies'),
    
    # Include router URLs
    path('', include(router.urls)),
]
