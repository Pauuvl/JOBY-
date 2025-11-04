from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    NotificationViewSet, PushNotificationTokenViewSet,
    NotificationPreferenceViewSet
)

router = DefaultRouter()
router.register(r'', NotificationViewSet, basename='notification')
router.register(r'push-tokens', PushNotificationTokenViewSet, basename='push-token')
router.register(r'preferences', NotificationPreferenceViewSet, basename='preference')

urlpatterns = [
    path('', include(router.urls)),
]
